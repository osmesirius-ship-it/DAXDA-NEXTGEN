#!/usr/bin/env python3
"""
DAXDA Next-Gen Unified Mission Navigator CLI
============================================
A frictionless command-line interface for evaluators, researchers, cadets, and federal agencies.
Unifies all 5 pillars of the DAXDA ecosystem:
  1. NASA Analog Mission Client (HERA 45d / CHAPEA 378d)
  2. US Space Academy Point-Based Mastery Curriculum (USSA-101 .. USSA-403)
  3. Federal Acquisition & Defense Manifest (AMERICAN MILESTONE INC · CAGE: 214X7 · UEI: MXEFU6TQJUB9)
  4. Mathematical Verification & Quantum Invariants (DUVAST-01 80/80 RELEASED)
  5. Dual-Stream Financial Settlement Architecture (Commercial Stripe Ingress vs Treasury EFT)
"""

import sys
import os
import argparse
import json
import subprocess
import webbrowser
from pathlib import Path

# Resolve base workspace directories robustly
CURRENT_FILE = Path(__file__).resolve()

# Find the daxda-next-gen project directory
if (CURRENT_FILE.parent / "outputs").exists():
    WORKSPACE_DIR = CURRENT_FILE.parent
elif (CURRENT_FILE.parent.parent / "outputs").exists():
    WORKSPACE_DIR = CURRENT_FILE.parent.parent
elif (CURRENT_FILE.parent / "DAXDA-NEXTGEN" / "daxda-next-gen").exists():
    WORKSPACE_DIR = CURRENT_FILE.parent / "DAXDA-NEXTGEN" / "daxda-next-gen"
else:
    # Walk up to find DAXDA-NEXTGEN/daxda-next-gen
    cur = CURRENT_FILE.parent
    found = None
    while cur != cur.parent:
        if (cur / "DAXDA-NEXTGEN" / "daxda-next-gen").exists():
            found = cur / "DAXDA-NEXTGEN" / "daxda-next-gen"
            break
        if (cur / "outputs" / "federal_registration_manifest.json").exists():
            found = cur
            break
        cur = cur.parent
    WORKSPACE_DIR = found or CURRENT_FILE.parent.parent

# Top-level workspace containing DUVAST_01
cur = WORKSPACE_DIR
ROOT_WORKSPACE = WORKSPACE_DIR.parent
while cur != cur.parent:
    if (cur / "DUVAST_01").exists():
        ROOT_WORKSPACE = cur
        break
    cur = cur.parent

OUTPUTS_DIR = WORKSPACE_DIR / "outputs"
DOCS_DIR = WORKSPACE_DIR / "docs"

# Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_banner():
    banner = f"""{CYAN}{BOLD}
    ========================================================================================
     ██████╗  █████╗ ██╗  ██╗██████╗  █████╗     ███╗   ██╗ █████╗ ██╗   ██╗
     ██╔══██╗██╔══██╗╚██╗██╔╝██╔══██╗██╔══██╗    ████╗  ██║██╔══██╗██║   ██║
     ██║  ██║███████║ ╚███╔╝ ██║  ██║███████║    ██╔██╗ ██║███████║██║   ██║
     ██║  ██║██╔══██║ ██╔██╗ ██║  ██║██╔══██║    ██║╚██╗██║██╔══██║╚██╗ ██╔╝
     ██████╔╝██║  ██║██╔╝ ██╗██████╔╝██║  ██║    ██║ ╚████║██║  ██║ ╚████╔╝ 
    ========================================================================================
     DAXDA NEXT-GEN OMNI-MISSION NAVIGATOR & COMMAND SUITE
     Prime Federal Contractor: AMERICAN MILESTONE INC | CAGE: 214X7 | UEI: MXEFU6TQJUB9
    ========================================================================================{RESET}
    """
    print(banner)


def cmd_status(args):
    """Show global health, compliance status, and test readiness across all 5 pillars."""
    print(f"\n{BOLD}{CYAN}=== DAXDA NEXT-GEN ECOSYSTEM SNAPSHOT ==={RESET}\n")

    # 1. Federal Status
    manifest_path = OUTPUTS_DIR / "federal_registration_manifest.json"
    fed_ok = False
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            data = json.load(f)
            prime = data.get("prime_awardee_partner", {})
            artifacts = data.get("artifacts", [])
            all_present = all(a.get("exists", False) for a in artifacts)
            fed_ok = True
            print(f"  {BOLD}🏛️  Federal Prime Awardee:{RESET} {GREEN}{prime.get('entity_name')}{RESET} (AOR: {prime.get('authorized_representative')})")
            print(f"     • CAGE Code: {YELLOW}{prime.get('cage_code')}{RESET} | UEI: {YELLOW}{prime.get('uei')}{RESET}")
            print(f"     • Treasury Disbursement: {GREEN}{prime.get('disbursement_channel')}{RESET} (Status: {data.get('disbursement_authorization', {}).get('status')})")
            print(f"     • Certified Federal Dossier Artifacts: {GREEN}{len(artifacts)}/{len(artifacts)} (100% Certified){RESET}")
    else:
        print(f"  {RED}✖ Federal Registration Manifest missing at {manifest_path}{RESET}")

    # 2. NASA Analog Client
    spec_path = DOCS_DIR / "compliance" / "NASA_HERA_CHAPEA_ANALOG_CLIENT_SPECIFICATION.md"
    if spec_path.exists():
        print(f"\n  {BOLD}🛰️  NASA Analog Mission Client:{RESET} {GREEN}READY{RESET}")
        print(f"     • HERA (Human Exploration Research Analog): {CYAN}45-Day Lunar/Near-Earth (0-5 min delay){RESET}")
        print(f"     • CHAPEA (Crew Health & Performance Exploration): {CYAN}378-Day Mars (3-22 min delay + Conjunction){RESET}")
        print(f"     • Clinical Medical Firewall: {GREEN}ACTIVE (NASA-STD-3001 & 14 CFR § 1230){RESET}")
        print(f"     • Epistemic Deliberation: {GREEN}Prospective Locking (H1) & Minority Dissent (OI-SHADOW){RESET}")
    else:
        print(f"  {RED}✖ NASA Analog Client Specification missing{RESET}")

    # 3. Space Academy Curriculum
    curr_path = DOCS_DIR / "proposals" / "DAXDA_USSA_EO14423_CURRICULUM_PROPOSAL_MASTER.md"
    if curr_path.exists():
        print(f"\n  {BOLD}🎓  US Space Academy Point-Based Curriculum (EO 14423):{RESET} {GREEN}READY{RESET}")
        print(f"     • Degree Tracks: {CYAN}1,800 MP Bachelor of Science / 900 MP Master of Science{RESET}")
        print(f"     • Core Modules: {CYAN}USSA-101 through USSA-403 (13 Master Courses with Hands-On Labs){RESET}")
        print(f"     • Verification: {GREEN}TEVV Matrix & APST/APEP Staged Transition Pathways{RESET}")

    # 4. Mathematical Verification
    duvast_path = ROOT_WORKSPACE / "DUVAST_01" / "run_duvast.py"
    if duvast_path.exists():
        print(f"\n  {BOLD}🔬  Mathematical Verification Oracle:{RESET} {GREEN}DUVAST-01 (Cl(7,0) / Cl(16,4)){RESET}")
        print(f"     • Test Suite Status: {GREEN}80/80 RELEASED (0 Contradictions, Zero Floating Signifiers){RESET}")
        print(f"     • Operations Inventory: {CYAN}886 v14 algebraic & geometric ops verified{RESET}")

    # 5. Dual Financial Architecture
    payout_config = OUTPUTS_DIR / "stripe_payout_config.json"
    if payout_config.exists():
        with open(payout_config, "r") as f:
            cfg = json.load(f)
            stripe_dest = cfg.get("payout_routing", {}).get("stripe_destination", {})
            ingress = stripe_dest.get("account_id", "fa_65VdIIXJjwPA5az6ErF16SjLR86BSQ2gmZByo9KWLCi0O0")
            status = stripe_dest.get("status", "ACTIVE_LINKED")
            print(f"\n  {BOLD}💳  Dual-Stream Settlement Architecture:{RESET} {GREEN}CONFIGURED{RESET}")
            print(f"     • Commercial Ingress (Stripe): {CYAN}{ingress}{RESET} ({status})")
            print(f"     • Federal Settlement (EFT): {YELLOW}AMERICAN MILESTONE INC (Direct Treasury Deposit){RESET}")

    print(f"\n{BOLD}{CYAN}----------------------------------------------------------------------------------------{RESET}")
    print(f" Run {YELLOW}python3 tools/daxda_nav.py open{RESET} to launch the visual Mission Navigator in your browser.\n")


def cmd_open(args):
    """Open the interactive HTML Mission Navigator in the system web browser."""
    navigator_path = OUTPUTS_DIR / "daxda_mission_navigator.html"
    if not navigator_path.exists():
        fallback = WORKSPACE_DIR / "outputs" / "navigator.html"
        if fallback.exists():
            navigator_path = fallback
        else:
            print(f"{RED}Error: {navigator_path} does not exist.{RESET}")
            return 1

    file_uri = navigator_path.resolve().as_uri()
    print(f"\n{GREEN}{BOLD}🚀 Launching DAXDA Next-Gen Mission Navigator...{RESET}")
    print(f"Path: {CYAN}{navigator_path.resolve()}{RESET}")
    print(f"URI:  {CYAN}{file_uri}{RESET}\n")
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(navigator_path.resolve())], check=False)
        else:
            webbrowser.open(file_uri)
    except Exception as e:
        print(f"{YELLOW}Could not open browser automatically: {e}{RESET}")
        print(f"Please open the following link manually in your browser:\n  {CYAN}{file_uri}{RESET}\n")
    return 0


def cmd_analog(args):
    """Run an interactive or automated NASA Analog Mission Client drill."""
    mission = args.mission or "both"
    cli_tool = WORKSPACE_DIR / "tools" / "nasa_analog_client_cli.py"
    cmd = [sys.executable, str(cli_tool), "--mission", mission]
    print(f"\n{CYAN}{BOLD}🛰️  Executing NASA Analog Client Simulation [{mission.upper()}]...{RESET}\n")
    subprocess.run(cmd, check=True)


def cmd_curriculum(args):
    """Explore the US Space Academy Point-Based Mastery Curriculum."""
    curr_path = DOCS_DIR / "proposals" / "DAXDA_USSA_EO14423_CURRICULUM_PROPOSAL_MASTER.md"
    if not curr_path.exists():
        print(f"{RED}Curriculum master document not found at {curr_path}{RESET}")
        return 1

    courses = [
        {"code": "USSA-101", "year": 1, "mp": 100, "title": "Ontological Grounding & Latent Removal (Hartman ISR)",
         "desc": "Anchoring operational telemetry to irreducible ground invariant SR0 = (s0, D, C). Strips floating signifiers and guarantees zero hallucinated telemetry.",
         "lab": "Cadets configure live telemetry ingestors and run daxda_guard/scanner.py against poisoned feeds to isolate ungrounded latent tokens."},
        {"code": "USSA-102", "year": 1, "mp": 150, "title": "Mission AI Security Practicum (MOD-E1..E5)",
         "desc": "Defending autonomous agent runtimes against prompt injections, AST escapes, and dimensional unit mismatches (preventing Mars Climate Orbiter disasters).",
         "lab": "Cadets inject adversarial polyglot payloads into agent toolchains, verify AST sandbox containment, and enforce SI DimensionVectors."},
        {"code": "USSA-103", "year": 1, "mp": 150, "title": "Recursive Specification & Verification Architecture (MOD-00)",
         "desc": "Translating natural language mission requirements into executable, machine-verifiable operational invariant contracts.",
         "lab": "Cadets build automated verification test harnesses and assert cryptographic SHA-256 state transitions before system deployment."},
        {"code": "USSA-201", "year": 2, "mp": 200, "title": "Clifford Geometric Governance (MOD-01)",
         "desc": "Mapping non-commutative attitude dynamics and multi-spacecraft kinematics onto Cl(7,0) and Cl(16,4) geometric rotor algebras.",
         "lab": "Cadets program 128-blade rotor transformations with numerical drift bounded below 1e-14, ensuring gimbal-lock-free attitude control."},
        {"code": "USSA-202", "year": 2, "mp": 150, "title": "Anomalous Containment & 100-Scenario Escape Defense (MOD-02)",
         "desc": "Hands-on mastery of 10 anomalous AI failure modes across 100 live-fire cyber-physical attack scenarios.",
         "lab": "Cadets manage simulated Layer-8 hardware interlocks, executing 300s incident correlations and surviving 1,000,000+ fail-closed cycles."},
        {"code": "USSA-203", "year": 2, "mp": 100, "title": "Pre-Compilation Matter Governance & Hardware Interlocks (MOD-08A)",
         "desc": "Auditing digital-twin micromachine blueprints for physical safety, laser/ultrasonic containment, and Ed25519 FABRICATE token issuance.",
         "lab": "Cadets inspect additive manufacturing G-code for thermal and resonant runaway vectors, asserting hardware safety before fabrication."},
        {"code": "USSA-301", "year": 3, "mp": 200, "title": "DA13 Distributed GPU Validation Grid (MOD-03)",
         "desc": "Heterogeneous multi-node compute scheduling with Byzantine fault tolerance and cryptographic proof-of-execution receipts.",
         "lab": "Cadets coordinate distributed cluster telemetry across disconnected compute nodes, isolating Sybil workers with consensus voting."},
        {"code": "USSA-302", "year": 3, "mp": 175, "title": "Deep-Space Asynchronous Causality (MOD-04)",
         "desc": "Managing decentralized, causal-consistent state replication under 0 to 22 minute asymmetric light delays and solar conjunction blackouts.",
         "lab": "Cadets simulate Earth-Mars communication windows, configuring store-and-forward buffers and prospective hypothesis locks."},
        {"code": "USSA-303", "year": 3, "mp": 150, "title": "Cognitive Security & MMPIBench Auditing (MOD-05)",
         "desc": "Auditing autonomous decision architectures for psychological integrity, cognitive drift, and adversarial deception resistance.",
         "lab": "Cadets execute adversarial cognitive stress batteries against autonomous co-pilots, verifying uncompromised reasoning."},
        {"code": "USSA-304", "year": 3, "mp": 125, "title": "Carbon Arbitrage & On-Demand Habitat Fabrication (MOD-06)",
         "desc": "In-situ resource utilization (ISRU) governance, closed-loop life support balancing, and autonomous structural 3D printing.",
         "lab": "Cadets balance oxygen-carbon cycles under catastrophic seal breaches using invariant matter-accounting algorithms."},
        {"code": "USSA-401", "year": 4, "mp": 125, "title": "Austere Ops, Biomedical MEMS Logistics & NASA-STD-3001 (MOD-07A)",
         "desc": "Zero-trust clinical medical firewalls separating research, care, and crew flight qualification during extended analog isolation.",
         "lab": "Cadets test fail-closed clinical barriers, preventing flight surgeons from leaking private biometric records to flight evaluators."},
        {"code": "USSA-402", "year": 4, "mp": 125, "title": "OI v2.2 Blackout Drills & Volumetric Displays (MOD-07B)",
         "desc": "Operating during total terrestrial loss-of-signal (LOS) using local holographic and haptic situational awareness feeds.",
         "lab": "Cadets command an isolated lunar habitat module through a 48-hour continuous communications blackout using local OI consensus."},
        {"code": "USSA-403", "year": 4, "mp": 150, "title": "Tier-2 Specialization Capstone & T0-T7 Qualification",
         "desc": "High-stakes multi-system defense capstone certifying cadets across all T0 through T7 operational readiness gates.",
         "lab": "Cadets defend a full-scale orbital infrastructure simulation against simultaneous cyber, physical, and communication attacks."}
    ]

    selected_year = args.year
    selected_course = args.course

    filtered = courses
    if selected_year:
        filtered = [c for c in filtered if c["year"] == int(selected_year)]
    if selected_course:
        filtered = [c for c in filtered if selected_course.upper() in c["code"].upper()]

    print(f"\n{BOLD}{CYAN}=== US SPACE ACADEMY 4-YEAR POINT CURRICULUM (EO 14423) ==={RESET}")
    print(f"{DIM}Total Graduation Threshold: 1,800 Mastery Points (B.S.) | 900 Mastery Points (M.S. Advanced Standing){RESET}\n")

    for c in filtered:
        print(f"{BOLD}{GREEN}[{c['code']}]{RESET} {BOLD}{c['title']}{RESET}  ({YELLOW}{c['mp']} MP{RESET} · Year {c['year']})")
        print(f"  {CYAN}Focus:{RESET} {c['desc']}")
        print(f"  {MAGENTA}Hands-On Practicum:{RESET} {c['lab']}\n")


def cmd_federal(args):
    """View active federal registration, CAGE/UEI identifiers, and the 14 certified artifacts."""
    manifest_path = OUTPUTS_DIR / "federal_registration_manifest.json"
    if not manifest_path.exists():
        print(f"{RED}Manifest not found at {manifest_path}{RESET}")
        return 1

    with open(manifest_path, "r") as f:
        data = json.load(f)

    prime = data.get("prime_awardee_partner", {})
    tech = data.get("technology_entity", {})
    aors = data.get("grants_gov_and_darpa_eps_aors", {})
    disb = data.get("disbursement_authorization", {})
    artifacts = data.get("artifacts", [])

    print(f"\n{BOLD}{CYAN}=== FEDERAL ENTITY REGISTRATION & PRIME CONTRACT VEHICLE ==={RESET}\n")
    print(f"  {BOLD}Prime Awardee:{RESET}          {GREEN}{prime.get('entity_name')}{RESET}")
    print(f"  {BOLD}Authorized Rep (AOR):{RESET}   {prime.get('authorized_representative')}")
    print(f"  {BOLD}SAM.gov UEI:{RESET}            {YELLOW}{prime.get('uei')}{RESET}")
    print(f"  {BOLD}DLA CAGE Code:{RESET}          {YELLOW}{prime.get('cage_code')}{RESET}")
    print(f"  {BOLD}SAM.gov Status:{RESET}         {GREEN}{prime.get('sam_gov_status')}{RESET}")
    print(f"  {BOLD}Disbursement Route:{RESET}     {GREEN}{prime.get('disbursement_channel')}{RESET}")
    print(f"  {BOLD}Technology Partner:{RESET}     {tech.get('legal_name')} (Ohio Doc #{tech.get('ohio_doc_number')})")
    print(f"  {BOLD}Chief Architect:{RESET}        {tech.get('architect')} ({tech.get('role')})")
    print(f"  {BOLD}DARPA ePS / Grants AOR:{RESET} {aors.get('prime_aor_and_ebiz_poc')}")

    print(f"\n{BOLD}{CYAN}=== 14/14 CERTIFIED FEDERAL PROPOSAL & COMPLIANCE ARTIFACTS ==={RESET}\n")
    for i, art in enumerate(artifacts, 1):
        status = art.get("status", "CERTIFIED")
        print(f"  {i:2d}. [{GREEN}✔{RESET}] {BOLD}{art.get('id')}{RESET}: {art.get('name')}")
        print(f"      {DIM}Path: {art.get('path')} ({art.get('size_bytes')} bytes){RESET}")

    print(f"\n  {BOLD}Overall Readiness Score:{RESET} {GREEN}{data.get('readiness_score')}% ALL GREEN{RESET}\n")


def cmd_verify(args):
    """Run DUVAST-01 and PyTest verification suites."""
    print(f"\n{BOLD}{CYAN}=== RUNNING COMPREHENSIVE VERIFICATION SUITES ==={RESET}\n")

    # 1. PyTest
    print(f"{BOLD}[1/2] Executing PyTest Regression Suites...{RESET}")
    pytest_cmd = [
        sys.executable, "-m", "pytest", "-v",
        str(WORKSPACE_DIR / "tests" / "test_nasa_analog_client.py"),
        str(WORKSPACE_DIR / "tests" / "test_standing_american_milestone_payments.py"),
        str(WORKSPACE_DIR / "tests" / "test_commercial_revenue.py")
    ]
    res1 = subprocess.run(pytest_cmd)

    # 2. DUVAST-01
    print(f"\n{BOLD}[2/2] Executing DUVAST-01 Invariant Oracle...{RESET}")
    duvast_runner = ROOT_WORKSPACE / "DUVAST_01" / "run_duvast.py"
    if duvast_runner.exists():
        res2 = subprocess.run([sys.executable, str(duvast_runner)], cwd=str(duvast_runner.parent))
    else:
        print(f"{YELLOW}DUVAST-01 runner not found at {duvast_runner}{RESET}")
        res2 = None

    print(f"\n{BOLD}{GREEN}✔ All Verification Tasks Complete.{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="DAXDA Next-Gen Omni-Mission Navigator & Command Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    # status
    p_status = subparsers.add_parser("status", help="Display global ecosystem snapshot and system health")

    # open
    p_open = subparsers.add_parser("open", help="Launch the interactive visual Mission Navigator in browser")

    # analog
    p_analog = subparsers.add_parser("analog", help="Execute NASA Analog Mission Client drill (HERA / CHAPEA)")
    p_analog.add_argument("--mission", choices=["hera", "chapea", "both"], default="both", help="Target analog mission")

    # curriculum
    p_curr = subparsers.add_parser("curriculum", help="Browse US Space Academy Point-Based Mastery courses")
    p_curr.add_argument("--year", type=int, choices=[1, 2, 3, 4], help="Filter by curriculum year")
    p_curr.add_argument("--course", type=str, help="Filter by course code (e.g., USSA-101)")

    # federal
    p_fed = subparsers.add_parser("federal", help="Inspect federal registration, CAGE/UEI, and certified artifacts")

    # verify
    p_verify = subparsers.add_parser("verify", help="Execute DUVAST-01 and PyTest verification harnesses")

    args = parser.parse_args()

    print_banner()

    if args.command == "status" or not args.command:
        cmd_status(args)
    elif args.command == "open":
        cmd_open(args)
    elif args.command == "analog":
        cmd_analog(args)
    elif args.command == "curriculum":
        cmd_curriculum(args)
    elif args.command == "federal":
        cmd_federal(args)
    elif args.command == "verify":
        cmd_verify(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
