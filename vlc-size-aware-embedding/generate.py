from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.embed import bytes_to_bits, embed_size_aware
from src.metrics import average_metrics
from src.video_io import read_gray_video, synthetic_video, write_gray_video


def main() -> None:
    p = argparse.ArgumentParser(description="Generate vlc-size-aware-embedding challenge.")
    p.add_argument("--input", help="Optional input video. Frames are normalized to a small 8x8-block-aligned grayscale sequence.")
    p.add_argument("--flag", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--output", default="output")
    p.add_argument("--step", type=float, default=224.0)
    args = p.parse_args()

    out_dir = Path(args.output)
    (out_dir / "private").mkdir(parents=True, exist_ok=True)
    frames, fps = read_gray_video(args.input) if args.input else (synthetic_video(), 12.0)
    bits = bytes_to_bits(args.flag.encode("utf-8"))
    stego, used_indices = embed_size_aware(frames, bits, args.seed, args.step)
    write_gray_video(out_dir / "stego.mp4", stego, fps)

    public = {
        "challenge": "vlc-size-aware-embedding",
        "seed": args.seed,
        "flag_length_bytes": len(args.flag.encode("utf-8")),
        "q_step": args.step,
        "used_coefficients": len(used_indices),
        "used_position_indices": used_indices,
        "vlc_rule": "estimated_vlc_size(new_coef) <= estimated_vlc_size(old_coef)",
        "source": str(args.input) if args.input else "synthetic",
        "mode": "frame-DCT simulation with fake VLC size model",
    }
    private = {**public, "flag": args.flag, "metrics_pre_encode": average_metrics(frames, stego)}
    (out_dir / "public_config.json").write_text(json.dumps(public, indent=2), encoding="utf-8")
    (out_dir / "private" / "flag.txt").write_text(args.flag, encoding="utf-8")
    (out_dir / "private_config.json").write_text(json.dumps(private, indent=2), encoding="utf-8")
    print(json.dumps(private, indent=2))


if __name__ == "__main__":
    main()
