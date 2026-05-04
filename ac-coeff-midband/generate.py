from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.embed import DEFAULT_COEFFS, bytes_to_bits, embed_bits_ac
from src.metrics import average_metrics
from src.video_io import read_y_video, synthetic_video, write_y_video


def parse_coeffs(raw: str) -> list[tuple[int, int]]:
    if not raw:
        return DEFAULT_COEFFS
    return [tuple(map(int, item.split(","))) for item in raw.split(";")]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ac-coeff-midband challenge.")
    parser.add_argument("--input")
    parser.add_argument("--max-width", type=int, default=0, help="Resize input video to this width before embedding. 0 keeps original size.")
    parser.add_argument("--flag", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", default="output")
    parser.add_argument("--coeffs", default="")
    parser.add_argument("--step", type=float, default=64.0)
    args = parser.parse_args()

    out_dir = Path(args.output)
    private_dir = out_dir / "private"
    out_dir.mkdir(parents=True, exist_ok=True)
    private_dir.mkdir(parents=True, exist_ok=True)

    coeffs = parse_coeffs(args.coeffs)
    frames, fps, chroma = read_y_video(args.input, args.max_width) if args.input else (synthetic_video(), 12.0, None)
    bits = bytes_to_bits(args.flag.encode("utf-8"))
    stego = embed_bits_ac(frames, bits, args.seed, coeffs, args.step)
    write_y_video(out_dir / "stego.mp4", stego, fps, chroma)

    public_config = {
        "challenge": "ac-coeff-midband",
        "seed": args.seed,
        "flag_length_bytes": len(args.flag.encode("utf-8")),
        "coefficient_candidates": coeffs,
        "q_step": args.step,
        "source": str(args.input) if args.input else "synthetic",
        "max_width": args.max_width if args.input else None,
        "mode": "frame-DCT simulation, not codec-level MPEG",
    }
    private_config = {**public_config, "flag": args.flag, "metrics_pre_encode": average_metrics(frames, stego)}
    (out_dir / "hint.txt").write_text("The message is hidden in mid-frequency AC coefficients.\n", encoding="utf-8")
    (out_dir / "public_config.json").write_text(json.dumps(public_config, indent=2), encoding="utf-8")
    (private_dir / "flag.txt").write_text(args.flag, encoding="utf-8")
    (out_dir / "private_config.json").write_text(json.dumps(private_config, indent=2), encoding="utf-8")
    print(json.dumps(private_config, indent=2))


if __name__ == "__main__":
    main()
