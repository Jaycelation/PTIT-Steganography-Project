from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.embed import embed_robust
from src.metrics import average_metrics
from src.reencode import reencode_light
from src.video_io import synthetic_video, write_gray_video


def main() -> None:
    p = argparse.ArgumentParser(description="Generate robust-dc-ac-after-reencode challenge.")
    p.add_argument("--flag", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--repeat", type=int, default=5)
    p.add_argument("--reencode", action="store_true", help="Kept for compatibility; reencode is done by default.")
    p.add_argument("--output", default="output")
    p.add_argument("--dc-step", type=float, default=120.0)
    p.add_argument("--ac-step", type=float, default=96.0)
    args = p.parse_args()

    out_dir = Path(args.output)
    (out_dir / "private").mkdir(parents=True, exist_ok=True)
    frames = synthetic_video()
    stego = embed_robust(frames, args.flag, args.seed, args.repeat, args.dc_step, args.ac_step)
    clean = out_dir / "stego_clean.mp4"
    reencoded = out_dir / "stego_reencoded.mp4"
    write_gray_video(clean, stego, 12.0)
    reencode_mode = reencode_light(clean, reencoded)

    public = {
        "challenge": "robust-dc-ac-after-reencode",
        "seed": args.seed,
        "repeat": args.repeat,
        "flag_length_bytes": len(args.flag.encode("utf-8")),
        "dc_step": args.dc_step,
        "ac_step": args.ac_step,
        "reencode_mode": reencode_mode,
        "mode": "frame-DCT simulation with repetition and majority vote",
    }
    private = {**public, "flag": args.flag, "metrics_clean_pre_encode": average_metrics(frames, stego)}
    (out_dir / "public_config.json").write_text(json.dumps(public, indent=2), encoding="utf-8")
    (out_dir / "private" / "flag.txt").write_text(args.flag, encoding="utf-8")
    (out_dir / "private_config.json").write_text(json.dumps(private, indent=2), encoding="utf-8")
    print(json.dumps(private, indent=2))


if __name__ == "__main__":
    main()

