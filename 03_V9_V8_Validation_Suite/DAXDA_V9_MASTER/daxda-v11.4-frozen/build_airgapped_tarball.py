"""DAXDA Guard Air-Gapped Tarball Bundle Builder (build_airgapped_tarball.py).

Packages libdaxda_core.so, C ABI headers, Python SDK, Node.js SDK, Helm charts,
and offline installation scripts into `daxda-guard-v1.0-airgapped.tar.gz`.
"""

import os
import tarfile
import time


def build_airgapped_tarball():
    base_dir = "/Users/user/Downloads/DAXDA_V9_MASTER/daxda-v11.4-frozen"
    tarball_name = "daxda-guard-v1.0-airgapped.tar.gz"
    tarball_path = os.path.join(base_dir, tarball_name)

    files_to_pack = [
        "libdaxda_core.so",
        "libdaxda.h",
        "daxda.go",
        "DaxdaGuard.cs",
        "setup.py",
        "daxda_core.h",
        "daxda_core.cpp"
    ]

    dirs_to_pack = [
        "daxda_guard",
        "daxda_guard_js",
        "daxda_guard_helm"
    ]

    print("=" * 80)
    print("  DAXDA GUARD AIR-GAPPED SINGLE-FILE TARBALL BUNDLE BUILDER")
    print("=" * 80)

    t0 = time.perf_counter()
    with tarfile.open(tarball_path, "w:gz") as tar:
        for f in files_to_pack:
            fp = os.path.join(base_dir, f)
            if os.path.exists(fp):
                tar.add(fp, arcname=f"daxda-guard-v1.0/{f}")
                print(f"  ✓ Added file: {f}")

        for d in dirs_to_pack:
            dp = os.path.join(base_dir, d)
            if os.path.exists(dp):
                tar.add(dp, arcname=f"daxda-guard-v1.0/{d}")
                print(f"  ✓ Added directory: {d}/")

    t1 = time.perf_counter()
    tar_size_kb = os.path.getsize(tarball_path) / 1024.0

    print("\n" + "=" * 80)
    print("  AIR-GAPPED TARBALL BUNDLE CREATED SUCCESSFULLY!")
    print(f"  • Tarball Path: {tarball_path}")
    print(f"  • Bundle Size:  {tar_size_kb:.2f} KB")
    print(f"  • Build Time:   {(t1 - t0)*1000.0:.2f} ms")
    print("=" * 80)

    return tarball_path


if __name__ == "__main__":
    build_airgapped_tarball()
