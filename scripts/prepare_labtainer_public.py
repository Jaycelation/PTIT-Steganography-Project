from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LAB_NAME = "dc-ac-drift-extract"
CONTAINER_NAME = "steg"
BASE_CHALLENGE = "dc-ac-combined"


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


def copy_student_challenge(workspace: Path) -> None:
    src_challenge = REPO_ROOT / BASE_CHALLENGE
    dst_challenge = workspace
    dst_challenge.mkdir(parents=True, exist_ok=True)

    copy_file(src_challenge / "README.md", dst_challenge / "challenge_README.md")
    for name in ["requirements.txt", "solve.py"]:
        copy_file(src_challenge / name, dst_challenge / name)

    copy_tree(src_challenge / "src", dst_challenge / "src")

    out_src = src_challenge / "output"
    out_dst = dst_challenge / "output"
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
        "answer.txt",
    }
    forbidden_dirs = {"private", "__pycache__", ".pytest_cache"}
    for path in sorted(out_root.rglob("*"), reverse=True):
        if path.is_dir() and path.name in forbidden_dirs:
            shutil.rmtree(path)
        elif path.is_file() and (path.name in forbidden_names or path.suffix == ".pyc"):
            path.unlink()


def build_package(output_root: Path) -> None:
    template_root = REPO_ROOT / "labtainer" / LAB_NAME
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    copy_templates(template_root, output_root)

    workspace = output_root / CONTAINER_NAME / LAB_NAME
    workspace.mkdir(parents=True, exist_ok=True)

    for doc in ROOT_DOCS:
        src = REPO_ROOT / doc
        if src.exists():
            copy_file(src, workspace / "reference" / doc)

    copy_student_challenge(workspace)
    remove_forbidden_files(output_root)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the Labtainer student package for dc-ac-drift-extract.")
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "labtainer" / "build" / LAB_NAME),
        help="Output directory for the generated Labtainer lab.",
    )
    args = parser.parse_args()

    out_root = Path(args.output).resolve()
    build_package(out_root)
    print(f"Created Labtainer package at {out_root}")


if __name__ == "__main__":
    main()
