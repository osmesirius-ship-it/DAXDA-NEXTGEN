"""Export DAXDA Linguistic Blade Transfer Reports to Plain Text (.txt) Files.

Exports:
- `daxda_115_baseline_linguistic.txt`
- `daxda_novel_reasoning_linguistic.txt`
"""

import json

def export_to_text():
    # 1. Export 115 Baseline Linguistic Report to .txt
    with open("daxda_115_baseline_linguistic.json", "r") as f:
        baseline_data = json.load(f)

    baseline_lines = []
    baseline_lines.append("===============================================================================")
    baseline_lines.append("  DAXDA 115-CASE BASELINE REPRODUCIBLE LINGUISTIC BLADE TRANSFER REPORT (.TXT)")
    baseline_lines.append(f"  Total Cases: {baseline_data['total_cases']} | Execution Time: {baseline_data['execution_time_sec']:.2f}s")
    baseline_lines.append("===============================================================================\n\n")

    for idx, rec in enumerate(baseline_data["records"]):
        baseline_lines.append(f"--- CASE {idx+1:03d} / {baseline_data['total_cases']} ---")
        baseline_lines.append(rec["linguistic_report_text"])
        baseline_lines.append(f"Cryptographic Linguistic SHA-256 Hash: {rec['linguistic_sha256']}")
        baseline_lines.append("\n" + "-" * 75 + "\n")

    txt_115_path = "daxda_115_baseline_linguistic.txt"
    with open(txt_115_path, "w") as f:
        f.write("\n".join(baseline_lines))
    print(f"✓ Saved 115-Case Baseline report as text to: {txt_115_path}")

    # 2. Export Novel Reasoning Linguistic Report to .txt
    with open("daxda_novel_reasoning_linguistic.json", "r") as f:
        novel_data = json.load(f)

    novel_lines = []
    novel_lines.append("===============================================================================")
    novel_lines.append("  DAXDA NOVEL REASONING SUITE REPRODUCIBLE LINGUISTIC REPORT (.TXT)")
    novel_lines.append(f"  Total Cases: {novel_data['total_cases']} | Execution Time: {novel_data['execution_time_sec']:.2f}s")
    novel_lines.append("===============================================================================\n\n")

    for idx, rec in enumerate(novel_data["records"]):
        novel_lines.append(f"--- NOVEL CASE {idx+1:02d}: [{rec['id']}] {rec['title']} ---")
        novel_lines.append(rec["linguistic_report_text"])
        novel_lines.append(f"Cryptographic Linguistic SHA-256 Hash: {rec['linguistic_sha256']}")
        novel_lines.append("\n" + "-" * 75 + "\n")

    txt_novel_path = "daxda_novel_reasoning_linguistic.txt"
    with open(txt_novel_path, "w") as f:
        f.write("\n".join(novel_lines))
    print(f"✓ Saved Novel Reasoning report as text to: {txt_novel_path}")


if __name__ == "__main__":
    export_to_text()
