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
    parser = argparse.ArgumentParser(description="Extract and validate the DC header marker.")
    parser.add_argument("--input", default="output/stego.mp4")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--output", default="work/header.log")
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    frames, _ = read_gray_video(args.input)
    magic = extract_stream(frames, int(cfg["seed"]), int(cfg["magic_length_bytes"]), "dc", float(cfg["dc_step"]))
    if magic != "STEG":
        raise SystemExit(f"Unexpected DC header: {magic!r}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"DC_HEADER_OK\nmagic={magic}\n", encoding="utf-8")
    print("DC_HEADER_OK")


if __name__ == "__main__":
    main()
