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
    parser = argparse.ArgumentParser(description="Report deterministic brute-force metrics.")
    parser.add_argument("--input", default="output/stego.mp4")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--recovered-config", default="work/recovered_config.json")
    parser.add_argument("--output", default="work/metrics.json")
    args = parser.parse_args()

    frames, fps = read_gray_video(args.input)
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    brute = cfg["bruteforce"]
    height, width = frames[0].shape
    blocks_per_frame = (height // 8) * (width // 8)
    coeffs_per_block = len(cfg.get("coefficient_candidates", []))
    seed_count = int(brute["seed_max"]) - int(brute["seed_min"]) + 1
    profiles = brute["coefficient_profiles"]
    data = {
        "marker": "METRICS_OK",
        "challenge": "dc-ac-bruteforce-extract",
        "source_model": "frame-DCT simulation, not codec-level MPEG",
        "width": width,
        "height": height,
        "frames": len(frames),
        "fps": fps,
        "dc_step": cfg["dc_step"],
        "ac_step": cfg["ac_step"],
        "magic_length_bytes": cfg["magic_length_bytes"],
        "flag_length_bytes": cfg["flag_length_bytes"],
        "seed_candidates": seed_count,
        "coefficient_profile_candidates": len(profiles),
        "total_candidates": seed_count * len(profiles),
        "estimated_ac_capacity_bits": len(frames) * blocks_per_frame * max(coeffs_per_block, 1),
    }
    recovered_path = Path(args.recovered_config)
    if recovered_path.exists():
        recovered = json.loads(recovered_path.read_text(encoding="utf-8"))
        data["recovered_seed"] = recovered.get("seed")
        data["coefficient_profile_index"] = recovered.get("bruteforce_result", {}).get("coefficient_profile_index")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("METRICS_OK")


if __name__ == "__main__":
    main()
