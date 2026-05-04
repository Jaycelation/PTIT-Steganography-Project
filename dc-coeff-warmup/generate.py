from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.embed import bytes_to_bits, embed_bits_dc
from src.metrics import average_metrics
from src.video_io import read_y_video, synthetic_video, write_y_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dc-coeff-warmup challenge.")
    parser.add_argument("--input", help="Optional input video.")
    parser.add_argument("--flag", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", default="output")
    parser.add_argument("--step", type=float, default=96.0)
    args = parser.parse_args()

    out_dir = Path(args.output)
    public_dir = out_dir / "public"
    private_dir = out_dir / "private"
    public_dir.mkdir(parents=True, exist_ok=True)
    private_dir.mkdir(parents=True, exist_ok=True)

    frames, fps, chroma = read_y_video(args.input) if args.input else (synthetic_video(), 12.0, None)
    bits = bytes_to_bits(args.flag.encode("utf-8"))
    stego = embed_bits_dc(frames, bits, args.seed, args.step)

    stego_path = out_dir / "stego.mp4"
    write_y_video(stego_path, stego, fps, chroma)

    metrics = average_metrics(frames, stego)
    config = {
        "challenge": "dc-coeff-warmup",
        "seed": args.seed,
        "flag_length_bytes": len(args.flag.encode("utf-8")),
        "bit_length": len(bits),
        "step": args.step,
        "source": str(args.input) if args.input else "synthetic",
        "mode": "frame-DCT simulation, not codec-level MPEG",
        "metrics_pre_encode": metrics,
    }
    (private_dir / "flag.txt").write_text(args.flag, encoding="utf-8")
    (private_dir / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    (public_dir / "README.md").write_text(
        "\n".join(
            [
                "# dc-coeff-warmup public notes",
                "",
                f"seed: {args.seed}",
                f"flag_length_bytes: {len(args.flag.encode('utf-8'))}",
                "rule: bits are embedded in the DC coefficient of selected 8x8 DCT blocks.",
                "model: frame-DCT simulation, not codec-level MPEG bitstream editing.",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    main()
