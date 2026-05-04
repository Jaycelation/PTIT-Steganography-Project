from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.drift import apply_compensation_base, simulate_uncompensated_drift
from src.embed import bytes_to_bits, embed_bits
from src.metrics import average_metrics
from src.video_io import read_y_video, synthetic_video, write_y_video


def main() -> None:
    p = argparse.ArgumentParser(description="Generate drift-compensation-basic challenge.")
    p.add_argument("--input", help="Optional input video. Embedding uses the Y channel and preserves chroma.")
    p.add_argument("--max-width", type=int, default=0, help="Resize input video to this width before embedding. 0 keeps original size.")
    p.add_argument("--flag", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--output", default="output")
    p.add_argument("--mode", choices=["no-compensation", "compensation", "both"], default="both")
    p.add_argument("--step", type=float, default=80.0)
    args = p.parse_args()

    out_dir = Path(args.output)
    (out_dir / "private").mkdir(parents=True, exist_ok=True)
    frames, fps, chroma = read_y_video(args.input, args.max_width) if args.input else (synthetic_video(), 12.0, None)
    bits = bytes_to_bits(args.flag.encode("utf-8"))

    embedded_plain = embed_bits(frames, bits, args.seed, args.step)
    stego_no_comp = simulate_uncompensated_drift(frames, embedded_plain)
    comp_base = apply_compensation_base(frames)
    stego_comp = embed_bits(comp_base, bits, args.seed, args.step)

    if args.mode in {"no-compensation", "both"}:
        write_y_video(out_dir / "stego_no_comp.mp4", stego_no_comp, fps, chroma)
    if args.mode in {"compensation", "both"}:
        write_y_video(out_dir / "stego_comp.mp4", stego_comp, fps, chroma)

    config = {
        "challenge": "drift-compensation-basic",
        "seed": args.seed,
        "flag_length_bytes": len(args.flag.encode("utf-8")),
        "step": args.step,
        "source": str(args.input) if args.input else "synthetic",
        "max_width": args.max_width if args.input else None,
        "mode": "frame-DCT simulation with predicted-frame drift model",
        "metrics_no_comp_pre_encode": average_metrics(frames, stego_no_comp),
        "metrics_comp_pre_encode": average_metrics(frames, stego_comp),
    }
    (out_dir / "public_config.json").write_text(json.dumps({k: v for k, v in config.items() if k != "flag"}, indent=2), encoding="utf-8")
    (out_dir / "private" / "flag.txt").write_text(args.flag, encoding="utf-8")
    (out_dir / "private_config.json").write_text(json.dumps({**config, "flag": args.flag}, indent=2), encoding="utf-8")
    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    main()
