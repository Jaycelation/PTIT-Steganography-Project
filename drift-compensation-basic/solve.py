from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.extract import extract_message
from src.video_io import read_gray_video


def main() -> None:
    p = argparse.ArgumentParser(description="Solve drift-compensation-basic challenge.")
    p.add_argument("--input", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--length", type=int, help="Flag length in bytes. Defaults to public_config.json next to input.")
    p.add_argument("--output", default="output/answer.txt")
    p.add_argument("--step", type=float, default=80.0)
    args = p.parse_args()

    length = args.length
    if length is None:
        cfg_path = Path(args.input).parent / "public_config.json"
        length = int(json.loads(cfg_path.read_text(encoding="utf-8"))["flag_length_bytes"])
    frames, _ = read_gray_video(args.input)
    answer = extract_message(frames, args.seed, length, args.step)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(answer, encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()
