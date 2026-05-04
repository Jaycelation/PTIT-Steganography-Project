from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.extract import extract_message_dc
from src.video_io import read_gray_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve dc-coeff-warmup challenge.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--length", type=int, required=True, help="Flag length in bytes.")
    parser.add_argument("--output", help="Optional answer file.")
    parser.add_argument("--step", type=float, help="QIM step. Defaults to config next to input, then 128.")
    args = parser.parse_args()

    frames, _ = read_gray_video(args.input)
    step = args.step
    if step is None:
        input_dir = Path(args.input).parent
        for cfg_path in (input_dir / "public_config.json", input_dir / "private" / "config.json"):
            if cfg_path.exists():
                step = float(json.loads(cfg_path.read_text(encoding="utf-8")).get("step", 128.0))
                break
    if step is None:
        step = 128.0
    answer = extract_message_dc(frames, args.seed, args.length, step)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(answer, encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()
