#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT))

from src.video_io import read_gray_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Report deterministic public metrics.")
    parser.add_argument("--input", default="output/stego.mp4")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--output", default="work/metrics.json")
    args = parser.parse_args()

    frames, fps = read_gray_video(args.input)
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    height, width = frames[0].shape
    blocks_per_frame = (height // 8) * (width // 8)
    coeffs_per_block = len(cfg.get("coefficient_candidates", []))
    data = {
        "marker": "METRICS_OK",
        "challenge": "ac-midband-extract",
        "source_model": "frame-DCT simulation, not codec-level MPEG",
        "width": width,
        "height": height,
        "frames": len(frames),
        "fps": fps,
        "q_step": cfg["q_step"],
        "flag_length_bytes": cfg["flag_length_bytes"],
        "estimated_ac_capacity_bits": len(frames) * blocks_per_frame * max(coeffs_per_block, 1),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("METRICS_OK")


if __name__ == "__main__":
    main()
