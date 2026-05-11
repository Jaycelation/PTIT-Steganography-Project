from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTAINER_NAME = "steg"


@dataclass(frozen=True)
class LabConfig:
    lab_name: str
    base_challenge: str


LABS = {
    "dc-ac-drift-extract": LabConfig("dc-ac-drift-extract", "dc-ac-combined"),
    "dc-ac-combined-extract": LabConfig("dc-ac-combined-extract", "dc-ac-combined"),
    "ac-midband-extract": LabConfig("ac-midband-extract", "ac-coeff-midband"),
}


ROOT_DOCS = [
    "README.md",
    "DEMO.md",
    "EVALUATION.md",
    "LABTAINER_READINESS.md",
    "LABTAINER_PROGRESS.md",
]


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Required source file is missing: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Required source directory is missing: {src}")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )


def copy_templates(template_root: Path, out_root: Path) -> None:
    for child in template_root.iterdir():
        target = out_root / child.name
        if child.is_dir():
            copy_tree(child, target)
        else:
            copy_file(child, target)


def copy_student_challenge(config: LabConfig, workspace: Path) -> None:
    src_challenge = REPO_ROOT / config.base_challenge
    workspace.mkdir(parents=True, exist_ok=True)

    copy_file(src_challenge / "README.md", workspace / "challenge_README.md")
    for name in ["requirements.txt", "solve.py"]:
        copy_file(src_challenge / name, workspace / name)

    copy_tree(src_challenge / "src", workspace / "src")

    out_src = src_challenge / "output"
    out_dst = workspace / "output"
    out_dst.mkdir(parents=True, exist_ok=True)
    for pattern in ["stego*.mp4", "public_config.json", "hint.txt"]:
        for item in out_src.glob(pattern):
            if item.is_file():
                copy_file(item, out_dst / item.name)

    public_notes = out_src / "public"
    if public_notes.exists():
        copy_tree(public_notes, out_dst / "public")


def remove_forbidden_files(out_root: Path) -> None:
    forbidden_names = {
        "generate.py",
        "checker.py",
        "private_config.json",
        "flag.txt",
        "answer.txt",
    }
    forbidden_dirs = {"private", "__pycache__", ".pytest_cache"}
    for path in sorted(out_root.rglob("*"), reverse=True):
        if path.is_dir() and path.name in forbidden_dirs:
            shutil.rmtree(path)
        elif path.is_file() and (path.name in forbidden_names or path.suffix == ".pyc"):
            if "work" not in path.parts:
                path.unlink()


def build_lab(config: LabConfig, output_root: Path) -> None:
    template_root = REPO_ROOT / "labtainer" / config.lab_name
    if not template_root.exists():
        raise FileNotFoundError(f"Labtainer template is missing: {template_root}")

    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    copy_templates(template_root, output_root)

    workspace = output_root / CONTAINER_NAME / config.lab_name
    workspace.mkdir(parents=True, exist_ok=True)

    for doc in ROOT_DOCS:
        src = REPO_ROOT / doc
        if src.exists():
            copy_file(src, workspace / "reference" / doc)

    copy_student_challenge(config, workspace)
    remove_forbidden_files(output_root)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Labtainer student packages for steganography labs.")
    parser.add_argument(
        "--lab",
        choices=[*LABS.keys(), "all"],
        default="all",
        help="Lab to build. Defaults to all Labtainer-ready labs.",
    )
    parser.add_argument(
        "--output-root",
        default=str(REPO_ROOT / "labtainer" / "build"),
        help="Root output directory for generated Labtainer labs.",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root).resolve()
    selected = LABS.values() if args.lab == "all" else [LABS[args.lab]]
    for config in selected:
        out = output_root / config.lab_name
        build_lab(config, out)
        print(f"Created Labtainer package at {out}")


if __name__ == "__main__":
    main()
