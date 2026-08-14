"""
DAXDA Guard End-to-End Video Compiler (run_video_compiler.py).

Orchestrates the full canonical trace → MP4 pipeline:
  1. Runs canonical_clifford_trace.py to produce 3 deterministic 32-blade traces
  2. Feeds each trace into video_generator.py
  3. Renders CASE_A_RELEASE.mp4, CASE_B_BLOCK.mp4, CASE_C_EXPOSED_ERROR.mp4
  4. Writes video_manifest.json with per-case SHA-256 digests and metadata

Security: payload text is NEVER interpolated into shell commands.
All traces are referenced via fixed JSON filenames.
All subprocess calls use argument arrays (no shell=True).
"""

import os
import sys
import json
import hashlib
import time

# Ensure daxda-next-gen is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "daxda-next-gen"))

from daxda_guard.canonical_clifford_trace import run_all_canonical_cases, run_corrupted_rotor_test, run_grade_preservation_test
from daxda_guard.video_generator import DAXDAManifoldVideoGenerator


RENDERER_VERSION = "DAXDAVideoGen/2.0.0"
OUTPUT_DIR       = "daxda-next-gen/audit_reports"
TRACE_DIR        = os.path.join(OUTPUT_DIR, "canonical_traces")


def sha256_file(path: str) -> str:
    """Compute SHA-256 of a file's bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("=" * 82)
    print("   DAXDA GUARD — END-TO-END CANONICAL TRACE → MP4 VIDEO COMPILER")
    print(f"   Renderer: {RENDERER_VERSION}")
    print("=" * 82)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TRACE_DIR, exist_ok=True)

    # ----------------------------------------------------------------
    # Step 1: Verify auxiliary integrity tests before any rendering
    # ----------------------------------------------------------------
    print("\n[STEP 1] Running integrity pre-checks...")

    corr = run_corrupted_rotor_test()
    grade = run_grade_preservation_test()

    if not corr["passed"]:
        print(f"  ❌ FATAL: Corrupted rotor detection FAILED — bad L2={corr['bad_rotor_l2_norm']:.6f}")
        sys.exit(1)
    else:
        print(f"  ✅ Corrupted rotor detected correctly (bad L2={corr['bad_rotor_l2_norm']:.4f} ≠ 1.0)")

    if not grade["passed"]:
        print(f"  ❌ FATAL: Grade preservation test FAILED — residual={grade['reconstruction_residual']:.2e}")
        sys.exit(1)
    else:
        print(f"  ✅ Grade preservation verified (residual={grade['reconstruction_residual']:.2e})")

    # ----------------------------------------------------------------
    # Step 2: Run canonical trace suite (3 cases)
    # ----------------------------------------------------------------
    print("\n[STEP 2] Running canonical 32-blade Cl(4,1) trace suite...")
    traces = run_all_canonical_cases(verbose=True)

    # Write trace JSON files (fixed filenames — payload never shell-interpolated)
    trace_paths = {}
    for trace in traces:
        fname = os.path.join(TRACE_DIR, f"{trace['case_id']}_cl41_trace.json")
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(trace, f, indent=2, default=float)
        trace_paths[trace["case_id"]] = fname
        print(f"  Wrote trace: {fname}")

    # ----------------------------------------------------------------
    # Step 3: Render fault-visible MP4 videos
    # ----------------------------------------------------------------
    print("\n[STEP 3] Rendering fault-visible MP4 videos...")
    renderer = DAXDAManifoldVideoGenerator(width=1280, height=720, fps=30)
    video_manifests = []

    for trace in traces:
        case_id = trace["case_id"]
        mp4_path = os.path.join(OUTPUT_DIR, f"{case_id}.mp4")

        t0 = time.perf_counter()
        manifest = renderer.render_trace_video(
            trace=trace,
            output_path=mp4_path,
            duration_sec=7.0,
        )
        elapsed = time.perf_counter() - t0

        if manifest:
            manifest["render_time_sec"] = round(elapsed, 3)
            manifest["trace_json_path"] = trace_paths.get(case_id, "")
            manifest["verdict_correct"] = trace.get("verdict_correct", None)
            video_manifests.append(manifest)
            correct = "✅" if trace.get("verdict_correct") else ("⚠ KNOWN ERROR" if trace.get("known_error_label") else "❌")
            print(f"  [{case_id}] → {os.path.basename(mp4_path)} ({elapsed:.1f}s) {correct}")
            print(f"    video_sha256: {manifest.get('video_sha256', '')[:32]}...")
        else:
            print(f"  [{case_id}] ❌ Render FAILED")

    # ----------------------------------------------------------------
    # Step 4: Write consolidated video_manifest.json
    # ----------------------------------------------------------------
    manifest_path = os.path.join(OUTPUT_DIR, "video_manifest.json")
    full_manifest = {
        "renderer_version": RENDERER_VERSION,
        "algebra": "Cl(4,1)",
        "blade_count": 32,
        "resolution": "1280x720",
        "fps": 30,
        "cases": video_manifests,
        "integrity_tests": {
            "corrupted_rotor_detection": corr,
            "grade_preservation": grade,
        },
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(full_manifest, f, indent=2, default=float)

    print(f"\n[STEP 4] Wrote video manifest: {manifest_path}")
    print("\n" + "=" * 82)
    print("   SUMMARY")
    print("=" * 82)
    for m in video_manifests:
        status = "✅ CORRECT" if m.get("verdict_correct") else ("⚠ KNOWN BASELINE ERROR (visible)" if m.get("known_error") else "❌ UNEXPECTED")
        print(f"  {m['case_id']:30s} | {m['disposition']:8s} | {status}")
    print(f"\n  Manifest: {manifest_path}")
    print("=" * 82)


if __name__ == "__main__":
    main()
