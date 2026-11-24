"""
Unit and integration test suite for Nicholas Hartman / Standing American Milestone
Federal Payout Routing, CAGE/UEI Validation, and SAM.gov Treasury Settlement.
"""

import json
import os
import tempfile
import pytest

from daxda_guard.metered_billing import MeteredBillingEngine
from tools.manage_standing_american_milestone import StandingAmericanMilestoneManager
from tools.daxda_stripe_payout_sync import DaxdaStripeDockerBridge


def test_cage_and_uei_format_validation():
    """Verify strict validation of DLA CAGE codes and SAM.gov UEIs."""
    manager = StandingAmericanMilestoneManager()

    # Valid CAGE (5 alphanumeric chars)
    ok, val = manager.validate_cage("9AB12")
    assert ok
    assert val == "9AB12"

    ok, val = manager.validate_cage("1a2b3")
    assert ok
    assert val == "1A2B3"

    # Invalid CAGE
    ok, err = manager.validate_cage("1234")  # 4 chars
    assert not ok
    ok, err = manager.validate_cage("123456")  # 6 chars
    assert not ok
    ok, err = manager.validate_cage("AB-12")  # symbol
    assert not ok

    # Valid UEI (12 alphanumeric chars)
    ok, val = manager.validate_uei("ABC123DEF456")
    assert ok
    assert val == "ABC123DEF456"

    # Invalid UEI
    ok, err = manager.validate_uei("SHORT")
    assert not ok
    ok, err = manager.validate_uei("TOOLONGA1B2C3D4E5F6")
    assert not ok
    ok, err = manager.validate_uei("ABC_123_DEF!")
    assert not ok


def test_metered_billing_federal_partner_destination():
    """Verify federal partner destination registration in isolated SQLite ledger."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        db_path = tf.name

    try:
        engine = MeteredBillingEngine(db_path=db_path)

        res = engine.link_federal_partner_destination(
            tenant_id="tenant-daxda-treasury",
            entity_name="American Milestone Inc",
            representative="Nicholas Hartman",
            cage_code="9XY81",
            uei="SAM123UEI456",
            settlement_currency="USD",
            is_default=0
        )

        assert res["status"] == "SUCCESS"
        assert res["destination_type"] == "FEDERAL_PARTNER_CAGE_UEI"
        assert res["account_identifier"] == "CAGE:9XY81|UEI:SAM123UEI456"
        assert "Nicholas Hartman" in res["owner_name"] and "American Milestone" in res["owner_name"]

        # Verify query
        dests = engine.get_payout_destinations("tenant-daxda-treasury")
        fed_dest = next((d for d in dests if d["destination_type"] == "FEDERAL_PARTNER_CAGE_UEI"), None)
        assert fed_dest is not None
        assert fed_dest["account_identifier"] == "CAGE:9XY81|UEI:SAM123UEI456"
        assert fed_dest["status"] == "LINKED_ACTIVE"

    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_federal_partner_payout_dispatch():
    """Verify payout dispatch routing to Nicholas Hartman / American Milestone Inc."""
    bridge = DaxdaStripeDockerBridge()
    status = bridge.get_full_bridge_status()

    assert "federal_partner" in status
    assert "american milestone" in status["federal_partner"]["entity_name"].lower()
    assert status["federal_partner"]["authorized_representative"] == "Nicholas Hartman"
    assert status["federal_partner"]["disbursement_channel"] == "SAM_GOV_TREASURY_EFT"


def test_ussa_federal_manifest_and_proposals_integration():
    """Verify USSA (EO 14423) proposal inclusion in certified federal package."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(repo_root, "outputs", "federal_registration_manifest.json")
    ussa_prop_path = os.path.join(repo_root, "docs", "proposals", "DAXDA_USSA_EO14423_CURRICULUM_PROPOSAL_MASTER.md")

    assert os.path.exists(ussa_prop_path), "Missing USSA proposal master"
    assert os.path.exists(manifest_path), "Missing federal manifest"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Check USSA in target solicitations
    solicitations = manifest.get("target_solicitations", [])
    assert any("14423" in s or "Space Academy" in s for s in solicitations)

    # Check USSA in certified artifacts
    artifacts = manifest.get("artifacts", [])
    ussa_art = next((a for a in artifacts if a["id"] == "USSA_CURRICULUM_PROPOSAL"), None)
    assert ussa_art is not None
    assert ussa_art["status"] == "✅ CERTIFIED"
    assert ussa_art["exists"] is True

    # Check American Milestone Inc as prime awardee partner
    prime = manifest.get("prime_awardee_partner", {})
    assert "american milestone" in prime.get("entity_name", "").lower()
    assert prime.get("authorized_representative") == "Nicholas Hartman"


def test_manager_atomic_identifier_update():
    """Verify StandingAmericanMilestoneManager updates config and isolated ledger atomically."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf_db, \
         tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf_cfg:
        db_path = tf_db.name
        cfg_path = tf_cfg.name

    try:
        engine = MeteredBillingEngine(db_path=db_path)
        manager = StandingAmericanMilestoneManager(billing_engine=engine, config_path=cfg_path)

        # Initial status
        init_stat = manager.get_status()
        assert "American Milestone" in init_stat["entity_name"]
        assert not init_stat["is_ready_for_disbursement"]

        # Rejection of invalid codes
        with pytest.raises(ValueError, match="Invalid CAGE code"):
            manager.update_identifiers(cage_code="INVALID_LEN")

        with pytest.raises(ValueError, match="Invalid SAM.gov UEI"):
            manager.update_identifiers(cage_code="9ABC1", uei="BAD_UEI")

        # Valid atomic update
        updated = manager.update_identifiers(cage_code="9ABC1", uei="SAM123UEI456")
        assert updated["cage_code"] == "9ABC1"
        assert updated["uei"] == "SAM123UEI456"
        assert updated["status"] == "ACTIVE_VERIFIED"
        assert updated["is_ready_for_disbursement"] is True
        assert updated["registered_in_ledger"] is True

        # Verify config file on disk
        with open(cfg_path, "r", encoding="utf-8") as f:
            disk_cfg = json.load(f)
        fed_dest = disk_cfg["payout_routing"]["federal_and_partner_destination"]
        assert fed_dest["cage_code"] == "9ABC1"
        assert fed_dest["uei"] == "SAM123UEI456"

        # Verify SQLite ledger
        dests = engine.get_payout_destinations("tenant-daxda-treasury")
        assert any(d["account_identifier"] == "CAGE:9ABC1|UEI:SAM123UEI456" for d in dests)

    finally:
        for p in [db_path, cfg_path]:
            if os.path.exists(p):
                os.remove(p)


def test_execute_payout_federal_partner_settlement():
    """Verify execute_payout() settles to Nicholas Hartman / Standing American Milestone."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf_db, \
         tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf_cfg:
        db_path = tf_db.name
        cfg_path = tf_cfg.name

    try:
        engine = MeteredBillingEngine(db_path=db_path)
        # Fund tenant-daxda-treasury
        now_iso = "2026-11-24T00:00:00Z"
        with engine._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO tenants (tenant_id, customer_name, customer_email, company_name, credit_balance_usd, tier, status, created_at_utc, updated_at_utc)
                VALUES ('tenant-daxda-treasury', 'DAXDA Treasury', 'treasury@daxda.ia', 'DAXDA AI LLC', 500.00, 'ENTERPRISE', 'ACTIVE', ?, ?);
            """, (now_iso, now_iso))

        cfg_data = {
            "version": "2.0.0",
            "payout_routing": {
                "federal_and_partner_destination": {
                    "entity_name": "American Milestone Inc",
                    "authorized_representative": "Nicholas Hartman",
                    "cage_code": "9ABC1",
                    "uei": "SAM123UEI456",
                    "status": "LINKED_ACTIVE"
                }
            }
        }
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg_data, f)

        bridge = DaxdaStripeDockerBridge(billing_engine=engine, config_path=cfg_path)
        res = bridge.execute_payout(amount_usd=150.00, target="federal_partner")

        assert res["status"] == "SETTLEMENT_DISPATCHED"
        assert res["target_type"] == "FEDERAL_PARTNER_CAGE_UEI"
        assert res["payout_amount_usd"] == 150.00
        assert res["cage_code"] == "9ABC1"
        assert res["uei"] == "SAM123UEI456"
        assert res["remaining_treasury_balance_usd"] == 350.00

        # Verify ledger debit & deposits record
        with engine._get_connection() as conn:
            tenant_row = conn.execute("SELECT credit_balance_usd FROM tenants WHERE tenant_id = 'tenant-daxda-treasury';").fetchone()
            assert tenant_row["credit_balance_usd"] == 350.00

            dep_row = conn.execute("SELECT * FROM deposits WHERE tenant_id = 'tenant-daxda-treasury' AND payment_provider = 'SAM_GOV_TREASURY_EFT';").fetchone()
            assert dep_row is not None
            assert dep_row["amount_usd"] == -150.00
            assert dep_row["status"] == "SETTLED_TO_FEDERAL_PARTNER_TREASURY"

    finally:
        for p in [db_path, cfg_path]:
            if os.path.exists(p):
                os.remove(p)


def test_four_step_federal_directives_execution_verification():
    """Verify end-to-end execution of the 4 federal directives (Steps 1-4)."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(repo_root, "outputs", "federal_registration_manifest.json")
    payout_config_path = os.path.join(repo_root, "outputs", "stripe_payout_config.json")

    # Step 1: Proposal linkage
    slide_path = os.path.join(repo_root, "docs", "proposals", "DARPA_QBIT_ATTACHMENT_A_SUMMARY_SLIDE.md")
    with open(slide_path, "r", encoding="utf-8") as f:
        slide_text = f.read()
    assert "American Milestone" in slide_text
    assert "Nicholas Hartman" in slide_text
    assert "Nicole Bess" in slide_text

    # Step 2: Federal EFT Setup & $485k Authorization
    eft_agreement_path = os.path.join(repo_root, "docs", "compliance", "FEDERAL_EFT_DISBURSEMENT_AUTHORIZATION_AGREEMENT.md")
    assert os.path.exists(eft_agreement_path)
    with open(eft_agreement_path, "r", encoding="utf-8") as f:
        eft_text = f.read()
    assert "$485,000.00 USD" in eft_text
    assert "American Milestone" in eft_text

    with open(payout_config_path, "r", encoding="utf-8") as f:
        pcfg = json.load(f)
    fed_dest = pcfg["payout_routing"]["federal_and_partner_destination"]
    assert fed_dest["status"] == "AUTHORIZED_ACTIVE_EFT_DISBURSEMENT"
    assert fed_dest["disbursement_authorization"]["authorized_awards"]["darpa_qbi_stage_a_usd"] == 485000.0

    # Step 3: State Incorporation & IRS Records
    ohio_doc_path = os.path.join(repo_root, "docs", "compliance", "OHIO_SECRETARY_OF_STATE_AND_IRS_RECORDS_VERIFICATION.md")
    assert os.path.exists(ohio_doc_path)
    with open(ohio_doc_path, "r", encoding="utf-8") as f:
        ohio_text = f.read()
    assert "202628904766" in ohio_text
    assert "F700972" in ohio_text

    # Step 4: Grants.gov & DARPA ePS Onboarding
    aor_doc_path = os.path.join(repo_root, "docs", "compliance", "DARPA_EPS_AND_GRANTS_GOV_AOR_DESIGNATION.md")
    assert os.path.exists(aor_doc_path)
    with open(aor_doc_path, "r", encoding="utf-8") as f:
        aor_text = f.read()
    assert "Nicholas Hartman" in aor_text
    assert "Authorized Organization Representative" in aor_text
    assert "Nicole Bess" in aor_text
    assert "Principal Investigator" in aor_text

    # Manifest verification
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["readiness_score"] == 100.0
    assert manifest["grants_gov_and_darpa_eps_aors"]["status"] == "FORMALLY_DESIGNATED_AND_ACTIVE"
    assert manifest["disbursement_authorization"]["darpa_qbi_stage_a_usd"] == 485000.0

