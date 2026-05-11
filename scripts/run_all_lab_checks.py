from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LAB_NAME = "dc-ac-drift-extract"


def run(cmd: list[str], cwd: Path) -> None:
    print(f"$ {' '.join(cmd)}")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(cmd, cwd=cwd, check=True, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local verification for the dc-ac-drift-extract Labtainer package.")
    parser.add_argument(
        "--package-root",
        default=str(REPO_ROOT / "labtainer" / "build" / LAB_NAME),
        help="Generated Labtainer package root.",
    )
    args = parser.parse_args()

    package_root = Path(args.package_root).resolve()
    lab_dir = package_root / "steg" / LAB_NAME
    if not lab_dir.exists():
        raise SystemExit(f"Generated lab directory does not exist: {lab_dir}")

    run([sys.executable, "tools/check_video_metadata.py"], cwd=lab_dir)
    run([sys.executable, "tools/run_dc_ac_extract.py"], cwd=lab_dir)
    run([sys.executable, "tools/report_metrics.py"], cwd=lab_dir)

    required = [
        lab_dir / "work" / "video_metadata.txt",
        lab_dir / "work" / "extract.log",
        lab_dir / "work" / "answer_status.txt",
        lab_dir / "work" / "answer.txt",
        lab_dir / "work" / "answer.sha256",
        lab_dir / "work" / "metrics.json",
    ]
    for item in required:
        if not item.exists() or not item.read_text(encoding="utf-8").strip():
            raise SystemExit(f"Missing or empty checkwork artifact: {item}")

    for cache_dir in package_root.rglob("__pycache__"):
        shutil.rmtree(cache_dir)

    forbidden_patterns = [
        "generate.py",
        "checker.py",
        "private_config.json",
        "answer.txt",
    ]
    leaks = []
    for path in package_root.rglob("*"):
        if path.is_dir() and path.name in {"private", "__pycache__"}:
            leaks.append(path)
        if path.is_file() and (path.name in forbidden_patterns or path.suffix == ".pyc"):
            if "work" not in path.parts:
                leaks.append(path)
    if leaks:
        formatted = "\n".join(str(x) for x in leaks)
        raise SystemExit(f"Forbidden files found in student package:\n{formatted}")

    print("LAB_CHECKS_OK")


if __name__ == "__main__":
    main()
