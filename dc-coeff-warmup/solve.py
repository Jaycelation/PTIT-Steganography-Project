from __future__ import annotations

import argparse
from pathlib import Path

from src.extract import extract_message_dc
from src.video_io import read_gray_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve dc-coeff-warmup challenge.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--length", type=int, required=True, help="Flag length in bytes.")
    parser.add_argument("--output", help="Optional answer file.")
    parser.add_argument("--step", type=float, default=128.0)
    args = parser.parse_args()

    frames, _ = read_gray_video(args.input)
    answer = extract_message_dc(frames, args.seed, args.length, args.step)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(answer, encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()
