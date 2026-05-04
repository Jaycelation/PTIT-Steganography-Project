from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.embed import AC_COEFFS, MAGIC, embed_combined
from src.metrics import average_metrics
from src.video_io import read_y_video, synthetic_video, write_y_video


def main() -> None:
    p = argparse.ArgumentParser(description="Generate dc-ac-combined challenge.")
    p.add_argument("--input", help="Optional input video. Embedding uses the Y channel and preserves chroma.")
    p.add_argument("--max-width", type=int, default=0, help="Resize input video to this width before embedding. 0 keeps original size.")
    p.add_argument("--flag", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--output", default="output")
    p.add_argument("--dc-step", type=float, default=96.0)
    p.add_argument("--ac-step", type=float, default=64.0)
    args = p.parse_args()

    out_dir = Path(args.output)
    (out_dir / "private").mkdir(parents=True, exist_ok=True)
    frames, fps, chroma = read_y_video(args.input, args.max_width) if args.input else (synthetic_video(), 12.0, None)
    stego = embed_combined(frames, args.flag, args.seed, args.dc_step, args.ac_step)
    write_y_video(out_dir / "stego.mp4", stego, fps, chroma)

    public = {
        "challenge": "dc-ac-combined",
        "seed": args.seed,
        "magic_length_bytes": len(MAGIC),
        "flag_length_bytes": len(args.flag.encode("utf-8")),
        "dc_step": args.dc_step,
        "ac_step": args.ac_step,
        "coefficient_candidates": AC_COEFFS,
        "source": str(args.input) if args.input else "synthetic",
        "max_width": args.max_width if args.input else None,
        "mode": "frame-DCT simulation, not codec-level MPEG",
    }
    private = {**public, "flag": args.flag, "magic": MAGIC, "metrics_pre_encode": average_metrics(frames, stego)}
    (out_dir / "public_config.json").write_text(json.dumps(public, indent=2), encoding="utf-8")
    (out_dir / "private_config.json").write_text(json.dumps(private, indent=2), encoding="utf-8")
    (out_dir / "private" / "flag.txt").write_text(args.flag, encoding="utf-8")
    print(json.dumps(private, indent=2))


if __name__ == "__main__":
    main()
