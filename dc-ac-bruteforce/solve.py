from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.extract import extract_flag
from src.video_io import read_gray_video


def main() -> None:
    p = argparse.ArgumentParser(description="Solve dc-ac-bruteforce challenge from a recovered config.")
    p.add_argument("--input", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output", default="output/answer.txt")
    args = p.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    missing = [name for name in ("seed", "ac_step") if name not in cfg]
    if missing:
        raise SystemExit(
            "Recovered config is missing required brute-force fields: "
            + ", ".join(missing)
        )
    coeffs = [tuple(x) for x in cfg["coefficient_candidates"]]
    frames, _ = read_gray_video(args.input)
    magic, flag = extract_flag(frames, int(cfg["seed"]), int(cfg["flag_length_bytes"]), float(cfg["dc_step"]), float(cfg["ac_step"]), coeffs)
    expected_magic = cfg.get("expected_magic") or cfg.get("bruteforce", {}).get("expected_magic", "STEG")
    if magic != expected_magic:
        raise SystemExit(f"Unexpected DC magic {magic!r}; expected {expected_magic!r}")
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(flag, encoding="utf-8")
    print(flag)


if __name__ == "__main__":
    main()
