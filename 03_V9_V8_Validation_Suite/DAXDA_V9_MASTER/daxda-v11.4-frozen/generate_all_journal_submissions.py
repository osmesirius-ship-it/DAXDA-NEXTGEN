"""Batch Scientific Journal Submission Generator.

Generates standalone, fully expanded, publication-grade scientific journal submission papers (.md)
for every single solved problem across:
1. The 115 Baseline Cognitive Suite (115 Papers)
2. The 14 Treasure Box Location Puzzles (14 Papers)
3. The 4 Novel Zero-Shot Reasoning Suite (4 Papers)

All manuscripts are saved in `/Users/user/Downloads/DAXDA_V9_MASTER/daxda-v11.4-frozen/journal_submissions/`.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List

from cl_n import CliffordAlgebra
from daxda_engine_nextgen import DAXDAEngineNextGen
from scientific_journal_report import ScientificJournalReportGenerator
from run_115_baseline_test import generate_115_test_cases
from daxda_nextgen_box_locations_test import TREASURE_BOX_PUZZLES


def generate_all_journal_manuscripts():
    output_dir = "/Users/user/Downloads/DAXDA_V9_MASTER/daxda-v11.4-frozen/journal_submissions"
    os.makedirs(output_dir, exist_ok=True)

    engine = DAXDAEngineNextGen(p=7, q=0)  # Cl(7,0) 128-Blade Multivector Space
    
    print("=" * 85)
    print("  DAXDA BATCH SCIENTIFIC JOURNAL SUBMISSION MANUSCRIPT GENERATOR")
    print(f"  Target Output Directory: {output_dir}")
    print("=" * 85)

    generated_papers = []

    # -------------------------------------------------------------------------
    # SUITE 1: 115 Baseline Test Cases
    # -------------------------------------------------------------------------
    print("\n[SUITE 1] Generating Manuscripts for 115 Baseline Cases...")
    baseline_cases = generate_115_test_cases()
    case_count = 0

    for domain_name, test_list in baseline_cases.items():
        for item in test_list:
            case_count += 1
            filename = f"journal_paper_baseline_{case_count:03d}_{domain_name.replace(' ', '_').lower()}.md"
            filepath = os.path.join(output_dir, filename)

            res = engine.evaluate_with_journal_report(domain_name, item)
            jr = res.get("scientific_journal_report", {})
            manuscript_md = jr.get("manuscript_markdown", "")

            with open(filepath, "w") as f:
                f.write(manuscript_md)

            generated_papers.append({
                "suite": "115 Baseline",
                "case_id": case_count,
                "domain": domain_name,
                "filename": filename,
                "filepath": filepath,
                "sha256": jr.get("manuscript_sha256", "")
            })

    print(f"  ✓ Successfully generated {case_count} manuscripts for 115 Baseline cases.")

    # -------------------------------------------------------------------------
    # SUITE 2: 14 Treasure Box Location Puzzles
    # -------------------------------------------------------------------------
    print("\n[SUITE 2] Generating Manuscripts for 14 Treasure Box Puzzles...")
    for puzzle in TREASURE_BOX_PUZZLES:
        cid = puzzle["case_id"]
        name = puzzle["name"]
        text = puzzle["text"]
        
        safe_name = name.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "").lower()
        filename = f"journal_paper_treasure_case_{cid:02d}_{safe_name}.md"
        filepath = os.path.join(output_dir, filename)

        res = engine.evaluate_with_journal_report("Physics", text)
        jr = res.get("scientific_journal_report", {})
        manuscript_md = jr.get("manuscript_markdown", "")

        # Expand manuscript with treasure puzzle context
        expanded_header = f"""# Journal Submission Manuscript: Autonomous Spatial Cipher Resolution of {name}
**Target Journal:** International Journal of High-Dimensional Geographic & Spatial Invariants
**Engine Version:** `12.0.1-GOVERNED`
**Date of Formalization:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
**Cryptographic Document SHA-256:** `{jr.get('manuscript_sha256', '')}`

---

"""
        full_text = expanded_header + manuscript_md

        with open(filepath, "w") as f:
            f.write(full_text)

        generated_papers.append({
            "suite": "Treasure Puzzles",
            "case_id": cid,
            "domain": "Physics/Spatial",
            "filename": filename,
            "filepath": filepath,
            "sha256": jr.get("manuscript_sha256", "")
        })

    print(f"  ✓ Successfully generated 14 manuscripts for Treasure Puzzles.")

    # -------------------------------------------------------------------------
    # SUITE 3: 4 Novel Zero-Shot Reasoning Puzzles
    # -------------------------------------------------------------------------
    print("\n[SUITE 3] Generating Manuscripts for 4 Novel Zero-Shot Puzzles...")
    novel_puzzles = [
        {"id": 1, "title": "Quantum Bell State Entanglement", "domain": "Physics", "input": "Quantum state |psi> = 1/sqrt(2) * (|00> + |11>) density matrix rho = |psi><psi| in Cl(7,0)"},
        {"id": 2, "title": "Trefoil Knot Topological Winding", "domain": "Mathematics", "input": "Trefoil knot embedding gamma(t) = (sin(t)+2*sin(2t), cos(t)-2*cos(2t), -sin(3t))"},
        {"id": 3, "title": "Alias Free SIMD Loop Optimization", "domain": "Software Engineering", "input": "def vectorized_kernel(A, B, C, n): for i in prange(n): A[i] = B[i] * C[i]"},
        {"id": 4, "title": "Anisotropic FLRW Metric Geodesic", "domain": "Physics", "input": "FLRW Metric Tensor ds^2 = -c^2 dt^2 + a(t)^2 [dr^2/(1-kr^2) + r^2 dOmega^2]"}
    ]

    for nov in novel_puzzles:
        nid = nov["id"]
        title = nov["title"]
        dom = nov["domain"]
        inp = nov["input"]

        safe_title = title.replace(" ", "_").lower()
        filename = f"journal_paper_novel_case_{nid:02d}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)

        res = engine.evaluate_with_journal_report(dom, inp)
        jr = res.get("scientific_journal_report", {})
        manuscript_md = jr.get("manuscript_markdown", "")

        with open(filepath, "w") as f:
            f.write(manuscript_md)

        generated_papers.append({
            "suite": "Novel Zero-Shot",
            "case_id": nid,
            "domain": dom,
            "filename": filename,
            "filepath": filepath,
            "sha256": jr.get("manuscript_sha256", "")
        })

    print(f"  ✓ Successfully generated 4 manuscripts for Novel Zero-Shot puzzles.")

    # Save Master Index JSON
    index_path = os.path.join(output_dir, "journal_manuscripts_master_index.json")
    with open(index_path, "w") as f:
        json.dump({"total_manuscripts": len(generated_papers), "manuscripts": generated_papers}, f, indent=2)

    print("\n" + "=" * 85)
    print("  ALL SCIENTIFIC JOURNAL SUBMISSION MANUSCRIPTS GENERATED SUCCESSFULLY!")
    print(f"  • Total Individual Journal Manuscripts: {len(generated_papers)}")
    print(f"  • Output Directory: {output_dir}")
    print(f"  • Master Index Saved: {index_path}")
    print("=" * 85)


if __name__ == "__main__":
    generate_all_journal_manuscripts()
