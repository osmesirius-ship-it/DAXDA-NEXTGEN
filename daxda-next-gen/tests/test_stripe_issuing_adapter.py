"""
Unit & Conformance Test Suite: Stripe Issuing Virtual Card & Commerce Gateway
=============================================================================
Validates:
1. $2,300.00 Hard Spending Ceiling enforcement.
2. Apple Store merchant whitelisting.
3. Fail-closed human authorization gate (HUMAN_AUTH_TOKEN:NICOLE_BESS).
4. Ephemeral single-use card lifecycle (ACTIVE -> CONSUMED -> Non-reusable).
5. Cryptographic audit sealing.
"""

import os
import shutil
import tempfile
import pytest

from daxda_guard.actuator_boundary import (
    AuthoritativePolicyEngine,
    GovernanceDisposition,
    FailClosedReason,
)
from daxda_guard.stripe_issuing_adapter import (
    StripeIssuingCommerceAdapter,
    CardStatus,
)


@pytest.fixture
def policy_engine():
    return AuthoritativePolicyEngine(default_ttl_seconds=60.0)


@pytest.fixture
def issuing_adapter(policy_engine):
    return StripeIssuingCommerceAdapter(
        policy_engine=policy_engine,
        apple_spend_limit=2300.00
    )


class TestStripeIssuingCommerce:
    def test_stage_apple_order_within_2300_limit_succeeds(self, issuing_adapter):
        """Order under $2,300 limit stages successfully."""
        # 14" M4 MacBook Pro: $1,599 + $150 tax = $1,749
        ok, staged, msg = issuing_adapter.stage_apple_order(
            item_description="14-inch MacBook Pro M4 (Space Black, 16GB, 512GB)",
            subtotal_usd=1599.00,
            estimated_tax_usd=111.93
        )
        assert ok is True
        assert staged is not None
        assert staged.total_amount_usd == 1710.93
        assert staged.total_amount_usd <= 2300.00
        assert "Order staged successfully" in msg

    def test_stage_order_exceeding_2300_limit_fails_closed(self, issuing_adapter):
        """Order exceeding the $2,300 limit is rejected at the boundary."""
        # Mac Pro or fully loaded maxed configuration over $2,300
        ok, staged, msg = issuing_adapter.stage_apple_order(
            item_description="Maxed Out Hardware Configuration",
            subtotal_usd=2400.00,
            estimated_tax_usd=168.00
        )
        assert ok is False
        assert staged is None
        assert "exceeds the authorized Apple spending limit of $2300.00 USD" in msg

    def test_mint_virtual_card_requires_human_authorization(self, issuing_adapter):
        """Minting virtual card without human authorization token fails closed."""
        ok, staged, _ = issuing_adapter.stage_apple_order(
            item_description="14-inch MacBook Pro M4",
            subtotal_usd=1599.00,
            estimated_tax_usd=111.93
        )

        ok_card, card, msg = issuing_adapter.mint_virtual_apple_card(
            order_id=staged.order_id,
            human_token=""  # Missing token
        )
        assert ok_card is False
        assert card is None
        assert "REQUIRE_EXPLICIT_HUMAN_AUTHORIZATION" in msg

    def test_mint_virtual_card_with_human_token_succeeds(self, issuing_adapter):
        """Minting with valid human token creates ephemeral card locked to Apple with $2,300 ceiling."""
        ok, staged, _ = issuing_adapter.stage_apple_order(
            item_description="14-inch MacBook Pro M4",
            subtotal_usd=1599.00,
            estimated_tax_usd=111.93
        )

        ok_card, card, msg = issuing_adapter.mint_virtual_apple_card(
            order_id=staged.order_id,
            human_token="HUMAN_AUTH_TOKEN:NICOLE_BESS"
        )
        assert ok_card is True
        assert card is not None
        assert card.spending_limit_usd == 2300.00
        assert card.cardholder_name == "Nicole Bess"
        assert card.status == CardStatus.ACTIVE_EPHEMERAL
        assert "Apple" in card.merchant_whitelist
        assert len(card.sha256_seal) == 64

    def test_execute_checkout_lifecycle_and_single_use(self, issuing_adapter):
        """Executing checkout marks the single-use card as CONSUMED and prevents reuse."""
        ok, staged, _ = issuing_adapter.stage_apple_order(
            item_description="14-inch MacBook Pro M4",
            subtotal_usd=1599.00,
            estimated_tax_usd=111.93
        )
        _, card, _ = issuing_adapter.mint_virtual_apple_card(
            order_id=staged.order_id,
            human_token="HUMAN_AUTH_TOKEN:NICOLE_BESS"
        )

        # Execute checkout
        ok_chk, confirm, msg = issuing_adapter.execute_apple_checkout(
            order_id=staged.order_id,
            card_id=card.card_id,
            human_token="HUMAN_AUTH_TOKEN:NICOLE_BESS"
        )
        assert ok_chk is True
        assert confirm["status"] == "ORDER_PLACED_CONFIRMED"
        assert confirm["amount_paid_usd"] == 1710.93
        assert card.status == CardStatus.CONSUMED

        # Attempt to reuse the consumed card: MUST FAIL
        ok_reuse, _, msg_reuse = issuing_adapter.execute_apple_checkout(
            order_id=staged.order_id,
            card_id=card.card_id,
            human_token="HUMAN_AUTH_TOKEN:NICOLE_BESS"
        )
        assert ok_reuse is False
        assert "CONSUMED" in msg_reuse
