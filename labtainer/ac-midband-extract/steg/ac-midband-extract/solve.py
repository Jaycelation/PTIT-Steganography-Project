from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.extract import extract_message_ac
from src.video_io import read_gray_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve ac-coeff-midband challenge.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    coeffs = [tuple(item) for item in config["coefficient_candidates"]]
    frames, _ = read_gray_video(args.input)
    answer = extract_message_ac(
        frames,
        int(config["seed"]),
        int(config["flag_length_bytes"]),
        coeffs,
        float(config["q_step"]),
    )
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(answer, encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

