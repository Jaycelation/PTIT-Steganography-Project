from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.extract import extract_message
from src.video_io import read_gray_video


def main() -> None:
    p = argparse.ArgumentParser(description="Solve vlc-size-aware-embedding challenge.")
    p.add_argument("--input", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--length", type=int)
    p.add_argument("--output", default="output/answer.txt")
    p.add_argument("--step", type=float)
    args = p.parse_args()

    cfg_path = Path(args.input).parent / "public_config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    length = args.length or int(cfg["flag_length_bytes"])
    step = args.step or float(cfg.get("q_step", 224.0))
    frames, _ = read_gray_video(args.input)
    answer = extract_message(frames, args.seed, length, step, cfg.get("used_position_indices"))
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(answer, encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()
