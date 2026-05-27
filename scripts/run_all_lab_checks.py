from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


LAB_CHECKS = {
    "dc-ac-drift-extract": [
        ["tools/check_video_metadata.py"],
        ["tools/run_dc_ac_extract.py"],
        ["tools/report_metrics.py"],
    ],
    "dc-ac-combined-extract": [
        ["tools/check_video_metadata.py"],
        ["tools/check_dc_header.py"],
        ["tools/run_dc_ac_extract.py"],
        ["tools/report_metrics.py"],
    ],
    "ac-midband-extract": [
        ["tools/check_video_metadata.py"],
        ["tools/check_ac_config.py"],
        ["tools/run_ac_extract.py"],
        ["tools/report_metrics.py"],
    ],
    "dc-ac-bruteforce-extract": [
        ["tools/check_video_metadata.py"],
        ["tools/audit_public_config.py"],
        ["tools/build_candidate_space.py"],
        ["tools/probe_dc_sync.py"],
        ["tools/run_bruteforce.py"],
        ["tools/run_bruteforce_extract.py"],
        ["tools/report_metrics.py"],
    ],
}


REQUIRED_FILES = {
    "dc-ac-drift-extract": [
        "work/video_metadata.txt",
        "work/extract.log",
        "work/answer_status.txt",
        "work/answer.txt",
        "work/answer.sha256",
        "work/metrics.json",
    ],
    "dc-ac-combined-extract": [
        "work/video_metadata.txt",
        "work/header.log",
        "work/extract.log",
        "work/answer_status.txt",
        "work/answer.txt",
        "work/answer.sha256",
        "work/metrics.json",
    ],
    "ac-midband-extract": [
        "work/video_metadata.txt",
        "work/ac_config.txt",
        "work/extract.log",
        "work/answer_status.txt",
        "work/answer.txt",
        "work/answer.sha256",
        "work/metrics.json",
    ],
    "dc-ac-bruteforce-extract": [
        "work/video_metadata.txt",
        "work/config_audit.txt",
        "work/candidates.json",
        "work/sync_probe.log",
        "work/bruteforce.log",
        "work/recovered_config.json",
        "work/extract.log",
        "work/answer_status.txt",
        "work/answer.txt",
        "work/answer.sha256",
        "work/metrics.json",
    ],
}


def run(cmd: list[str], cwd: Path) -> None:
    full_cmd = [sys.executable, *cmd]
    print(f"$ {' '.join(full_cmd)}")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(full_cmd, cwd=cwd, check=True, env=env)


def verify_no_forbidden_files(package_root: Path) -> None:
    for cache_dir in package_root.rglob("__pycache__"):
        shutil.rmtree(cache_dir)

    forbidden_names = {
        "generate.py",
        "checker.py",
        "private_config.json",
        "flag.txt",
    }
    leaks = []
    for path in package_root.rglob("*"):
        if path.is_dir() and path.name in {"private", "__pycache__"}:
            leaks.append(path)
        elif path.is_file() and (path.name in forbidden_names or path.suffix == ".pyc"):
            leaks.append(path)
        elif path.is_file() and path.name == "answer.txt" and "work" not in path.parts:
            leaks.append(path)
    if leaks:
        formatted = "\n".join(str(x) for x in leaks)
        raise SystemExit(f"Forbidden files found in student package:\n{formatted}")


def verify_lab(package_root: Path, lab_name: str) -> None:
    lab_dir = package_root / lab_name / "steg" / lab_name
    if not lab_dir.exists():
        raise SystemExit(f"Generated lab directory does not exist: {lab_dir}")

    for cmd in LAB_CHECKS[lab_name]:
        run(cmd, cwd=lab_dir)

    for item in REQUIRED_FILES[lab_name]:
        path = lab_dir / item
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise SystemExit(f"Missing or empty checkwork artifact: {path}")

    verify_no_forbidden_files(package_root / lab_name)
    print(f"{lab_name}: LAB_CHECKS_OK")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local verification for generated Labtainer packages.")
    parser.add_argument(
        "--package-root",
        default=str(REPO_ROOT / "labtainer" / "build"),
        help="Generated Labtainer package root.",
    )
    parser.add_argument("--lab", choices=[*LAB_CHECKS.keys(), "all"], default="all")
    args = parser.parse_args()

    package_root = Path(args.package_root).resolve()
    selected = LAB_CHECKS.keys() if args.lab == "all" else [args.lab]
    for lab_name in selected:
        verify_lab(package_root, lab_name)
    print("LAB_CHECKS_OK")


if __name__ == "__main__":
    main()
