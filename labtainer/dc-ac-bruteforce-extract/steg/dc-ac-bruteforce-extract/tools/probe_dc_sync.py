#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT))

from src.extract import extract_stream
from src.video_io import read_gray_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe candidate seeds for the DC sync marker.")
    parser.add_argument("--input", default="output/stego.mp4")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--output", default="work/sync_probe.log")
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    brute = cfg["bruteforce"]
    expected_magic = brute.get("expected_magic", "STEG")
    frames, _ = read_gray_video(args.input)
    matching_seeds: list[int] = []
    for seed in range(int(brute["seed_min"]), int(brute["seed_max"]) + 1):
        magic = extract_stream(frames, seed, int(cfg["magic_length_bytes"]), "dc", float(cfg["dc_step"]))
        if magic == expected_magic:
            matching_seeds.append(seed)

    if not matching_seeds:
        raise SystemExit("No seed produced the expected DC sync marker")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                "DC_SYNC_FOUND",
                f"expected_magic={expected_magic}",
                "matching_seeds=" + ",".join(str(seed) for seed in matching_seeds),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print("DC_SYNC_FOUND")


if __name__ == "__main__":
    main()
