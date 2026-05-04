from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.extract import extract_flag
from src.video_io import read_gray_video


def main() -> None:
    p = argparse.ArgumentParser(description="Solve dc-ac-combined challenge.")
    p.add_argument("--input", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output", default="output/answer.txt")
    args = p.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    coeffs = [tuple(x) for x in cfg["coefficient_candidates"]]
    frames, _ = read_gray_video(args.input)
    magic, flag = extract_flag(frames, int(cfg["seed"]), int(cfg["flag_length_bytes"]), float(cfg["dc_step"]), float(cfg["ac_step"]), coeffs)
    if magic != "STEG":
        print(f"warning: unexpected DC magic {magic!r}")
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(flag, encoding="utf-8")
    print(flag)


if __name__ == "__main__":
    main()

