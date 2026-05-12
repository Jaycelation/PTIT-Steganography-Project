from __future__ import annotations

import argparse
import shutil
import tarfile
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

    for name in ["requirements.txt", "solve.py"]:
        copy_file(src_challenge / name, workspace / name)

    copy_tree(src_challenge / "src", workspace / "src")

    out_src = src_challenge / "output"
    out_dst = workspace / "output"
    out_dst.mkdir(parents=True, exist_ok=True)
    copy_file(out_src / "stego.mp4", out_dst / "stego.mp4")
    copy_file(out_src / "public_config.json", out_dst / "public_config.json")
    hint = out_src / "hint.txt"
    if hint.exists():
        copy_file(hint, out_dst / "hint.txt")


def remove_forbidden_files(out_root: Path) -> None:
    forbidden_names = {
        "generate.py",
        "checker.py",
        "private_config.json",
        "flag.txt",
        "answer.txt",
        "answer.sha256",
        "answer_status.txt",
        "extract.log",
        "metrics.json",
    }
    forbidden_dirs = {"private", "work", "reference", "__pycache__", ".pytest_cache"}
    for path in sorted(out_root.rglob("*"), reverse=True):
        if path.is_dir() and path.name in forbidden_dirs:
            shutil.rmtree(path)
        elif path.is_file() and (path.name in forbidden_names or path.suffix == ".pyc"):
            path.unlink()


def normalize_tar_info(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
    tarinfo.uid = 0
    tarinfo.gid = 0
    tarinfo.uname = ""
    tarinfo.gname = ""
    if tarinfo.isdir():
        tarinfo.mode = 0o755
    elif "/_bin/" in f"/{tarinfo.name}" or tarinfo.name.endswith(".sh"):
        tarinfo.mode = 0o755
    else:
        tarinfo.mode = 0o644
    return tarinfo


def create_home_tar(lab_root: Path, lab_name: str) -> Path:
    steg_root = lab_root / CONTAINER_NAME
    tar_path = steg_root / f"{lab_name}.steg.student.tar.gz"
    if tar_path.exists():
        tar_path.unlink()

    required = [
        steg_root / "_bin",
        steg_root / "instructions.txt",
        steg_root / lab_name,
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(f"Required home tar entry is missing: {path}")

    with tarfile.open(tar_path, "w:gz") as tar:
        for path in required:
            tar.add(path, arcname=path.name, filter=normalize_tar_info)

    return tar_path


def create_sys_tar(lab_root: Path, lab_name: str) -> Path:
    steg_root = lab_root / CONTAINER_NAME
    tar_path = steg_root / f"sys_{lab_name}.steg.student.tar.gz"
    if tar_path.exists():
        tar_path.unlink()

    with tarfile.open(tar_path, "w:gz"):
        pass

    return tar_path


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

    copy_student_challenge(config, workspace)
    remove_forbidden_files(output_root)
    create_home_tar(output_root, config.lab_name)
    create_sys_tar(output_root, config.lab_name)


def create_lab_tar(lab_root: Path, tar_root: Path) -> Path:
    tar_root.mkdir(parents=True, exist_ok=True)
    tar_path = tar_root / f"{lab_root.name}.tar"
    if tar_path.exists():
        tar_path.unlink()

    with tarfile.open(tar_path, "w") as tar:
        tar.add(lab_root, arcname=lab_root.name)

    return tar_path


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
    parser.add_argument(
        "--tar-root",
        default=str(REPO_ROOT / "labtainer"),
        help="Directory where .tar archives are written.",
    )
    parser.add_argument(
        "--no-tar",
        action="store_true",
        help="Only prepare directories; do not write .tar archives.",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root).resolve()
    tar_root = Path(args.tar_root).resolve()
    selected = LABS.values() if args.lab == "all" else [LABS[args.lab]]
    for config in selected:
        out = output_root / config.lab_name
        build_lab(config, out)
        print(f"Created Labtainer package at {out}")
        if not args.no_tar:
            tar_path = create_lab_tar(out, tar_root)
            print(f"Created Labtainer tar at {tar_path}")


if __name__ == "__main__":
    main()
