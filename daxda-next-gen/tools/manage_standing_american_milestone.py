#!/usr/bin/env python3
"""
DAXDA Next-Gen — Standing American Milestone (Nicholas Hartman) CAGE & UEI Manager
===================================================================================
Manages federal awardee partner routing, SAM.gov registration identifiers, and
Treasury electronic funds transfer (EFT) payout destinations for:

  Prime Federal Contractor : Standing American Milestone
  Authorized Representative: Nicholas Hartman
  Identifiers              : DLA CAGE Code (5-chars) & SAM.gov UEI (12-chars)

Updates:
1. outputs/stripe_payout_config.json
2. outputs/billing_ledger.db (payout_destinations)
3. outputs/federal_registration_manifest.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from daxda_guard.metered_billing import get_billing_engine
from tools.prepare_darpa_and_federal_registration import main as regenerate_manifest

OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
CONFIG_PATH = os.path.join(OUTPUTS_DIR, "stripe_payout_config.json")
MANIFEST_PATH = os.path.join(OUTPUTS_DIR, "federal_registration_manifest.json")
DB_PATH = os.path.join(OUTPUTS_DIR, "billing_ledger.db")

CAGE_PATTERN = re.compile(r"^[A-Z0-9]{5}$")
UEI_PATTERN = re.compile(r"^[A-Z0-9]{12}$")


class StandingAmericanMilestoneManager:
    """Configures and validates Nicholas Hartman / Standing American Milestone federal routing."""

    def __init__(self, billing_engine=None, config_path: Optional[str] = None):
        self.billing_engine = billing_engine or get_billing_engine()
        self.config_path = config_path or CONFIG_PATH

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_config(self, cfg: Dict[str, Any]) -> None:
        out_dir = os.path.dirname(self.config_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

    def validate_cage(self, cage: str) -> Tuple[bool, str]:
        cleaned = cage.strip().upper()
        if not CAGE_PATTERN.match(cleaned):
            return False, f"Invalid CAGE code '{cage}'. Must be exactly 5 alphanumeric characters (e.g. '1ABC2')."
        return True, cleaned

    def validate_uei(self, uei: str) -> Tuple[bool, str]:
        cleaned = uei.strip().upper()
        if not UEI_PATTERN.match(cleaned):
            return False, f"Invalid SAM.gov UEI '{uei}'. Must be exactly 12 alphanumeric characters (e.g. 'ABC123DEF456')."
        return True, cleaned

    def get_status(self) -> Dict[str, Any]:
        cfg = self.load_config()
        payout_routing = cfg.get("payout_routing", {})
        fed_dest = payout_routing.get("federal_and_partner_destination", {})

        env_cage = os.environ.get("STANDING_AMERICAN_MILESTONE_CAGE", "")
        env_uei = os.environ.get("STANDING_AMERICAN_MILESTONE_UEI", "")

        active_cage = env_cage or fed_dest.get("cage_code", "PENDING_INPUT")
        active_uei = env_uei or fed_dest.get("uei", "PENDING_INPUT")

        # Check ledger
        ledger_destinations = self.billing_engine.get_payout_destinations("tenant-daxda-treasury")
        ledger_fed = next((d for d in ledger_destinations if d.get("destination_type") == "FEDERAL_PARTNER_CAGE_UEI"), None)

        is_ready = bool(
            active_cage != "PENDING_INPUT" and
            active_uei != "PENDING_INPUT" and
            CAGE_PATTERN.match(active_cage) and
            UEI_PATTERN.match(active_uei)
        )

        return {
            "entity_name": "Standing American Milestone",
            "authorized_representative": "Nicholas Hartman",
            "role": "Prime Federal Contractor & SAM.gov Awardee Vehicle",
            "cage_code": active_cage,
            "uei": active_uei,
            "disbursement_channel": "SAM_GOV_TREASURY_EFT",
            "status": "ACTIVE_VERIFIED" if is_ready else "CONFIGURED_PENDING_CONFIRMATION",
            "is_ready_for_disbursement": is_ready,
            "registered_in_ledger": bool(ledger_fed),
            "ledger_account_identifier": ledger_fed["account_identifier"] if ledger_fed else None,
            "config_file": self.config_path,
            "manifest_file": MANIFEST_PATH
        }

    def update_identifiers(
        self,
        cage_code: Optional[str] = None,
        uei: Optional[str] = None,
        is_default_for_federal: bool = True
    ) -> Dict[str, Any]:
        """Atomically updates CAGE and UEI across config, SQLite ledger, and federal manifest."""
        cfg = self.load_config()
        if "payout_routing" not in cfg:
            cfg["payout_routing"] = {}

        fed_dest = cfg["payout_routing"].get("federal_and_partner_destination", {})

        cur_cage = fed_dest.get("cage_code", "PENDING_INPUT")
        cur_uei = fed_dest.get("uei", "PENDING_INPUT")

        if cage_code is not None:
            valid, norm_cage = self.validate_cage(cage_code)
            if not valid:
                raise ValueError(norm_cage)
            cur_cage = norm_cage

        if uei is not None:
            valid, norm_uei = self.validate_uei(uei)
            if not valid:
                raise ValueError(norm_uei)
            cur_uei = norm_uei

        now_iso = datetime.now(timezone.utc).isoformat()

        cfg["version"] = "2.0.0"
        cfg["federal_partner_entity"] = "Standing American Milestone"
        cfg["federal_authorized_representative"] = "Nicholas Hartman"
        cfg["payout_routing"]["federal_and_partner_destination"] = {
            "provider": "SAM_GOV_TREASURY_EFT",
            "entity_name": "Standing American Milestone",
            "authorized_representative": "Nicholas Hartman",
            "cage_code": cur_cage,
            "uei": cur_uei,
            "disbursement_channel": "FEDERAL_EFT_AND_TREASURY",
            "settlement_currency": "USD",
            "status": "LINKED_ACTIVE",
            "is_default_for_federal_awards": is_default_for_federal,
            "updated_at_utc": now_iso
        }
        self.save_config(cfg)

        # Update SQLite ledger
        self.billing_engine.link_federal_partner_destination(
            tenant_id="tenant-daxda-treasury",
            entity_name="Standing American Milestone",
            representative="Nicholas Hartman",
            cage_code=cur_cage,
            uei=cur_uei,
            settlement_currency="USD",
            is_default=0
        )

        # Regenerate manifest if using production config
        if self.config_path == CONFIG_PATH:
            regenerate_manifest()

        return self.get_status()


def main():
    parser = argparse.ArgumentParser(description="Manage Standing American Milestone (Nicholas Hartman) Federal Payout Routing")
    parser.add_argument("--status", action="store_true", help="Display current Standing American Milestone federal routing status")
    parser.add_argument("--set-cage", type=str, help="Set 5-character DLA CAGE Code (e.g. 9ABC1)")
    parser.add_argument("--set-uei", type=str, help="Set 12-character SAM.gov Unique Entity Identifier (e.g. ABC123DEF456)")
    parser.add_argument("--link-ledger", action="store_true", help="Sync federal partner payout destination directly into billing ledger")
    args = parser.parse_args()

    manager = StandingAmericanMilestoneManager()

    if args.set_cage or args.set_uei:
        try:
            res = manager.update_identifiers(cage_code=args.set_cage, uei=args.set_uei)
            print("Successfully updated Standing American Milestone federal registration:")
            print(json.dumps(res, indent=2))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.link_ledger:
        status = manager.get_status()
        res = manager.update_identifiers(cage_code=status["cage_code"] if status["cage_code"] != "PENDING_INPUT" else None,
                                         uei=status["uei"] if status["uei"] != "PENDING_INPUT" else None)
        print("Synchronized Standing American Milestone with SQLite billing ledger:")
        print(json.dumps(res, indent=2))
        return

    # Default to status
    print(json.dumps(manager.get_status(), indent=2))


if __name__ == "__main__":
    main()
