#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import string
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_ROOT))

from src.extract import extract_flag
from src.video_io import read_gray_video


def is_printable(text: str) -> bool:
    allowed = set(string.printable)
    return bool(text) and all(ch in allowed for ch in text)


def score_candidate(text: str, prefix: str) -> int:
    score = 0
    if text.startswith(prefix):
        score += 100
    if text.endswith("}"):
        score += 25
    if is_printable(text):
        score += 25
    if "\ufffd" not in text:
        score += 10
    return score


def main() -> None:
    parser = argparse.ArgumentParser(description="Brute-force the hidden seed and AC coefficient profile.")
    parser.add_argument("--input", default="output/stego.mp4")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--candidates", default="work/candidates.json")
    parser.add_argument("--output", default="work/recovered_config.json")
    parser.add_argument("--log", default="work/bruteforce.log")
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    candidate_data = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    brute = cfg["bruteforce"]
    expected_magic = brute.get("expected_magic", "STEG")
    expected_prefix = brute.get("expected_prefix", "PTIT{")
    coeffs = [tuple(x) for x in cfg["coefficient_candidates"]]
    frames, _ = read_gray_video(args.input)

    tested = 0
    best: dict[str, object] | None = None
    best_score = -1
    for candidate in candidate_data["candidates"]:
        tested += 1
        seed = int(candidate["seed"])
        coeffs = [tuple(x) for x in candidate["coefficient_candidates"]]
        magic, recovered = extract_flag(
            frames,
            seed,
            int(cfg["flag_length_bytes"]),
            float(cfg["dc_step"]),
            float(cfg["ac_step"]),
            coeffs,
        )
        if magic != expected_magic:
            continue
        score = score_candidate(recovered, expected_prefix)
        if score > best_score:
            best_score = score
            best = {
                "seed": seed,
                "coefficient_profile_index": int(candidate["coefficient_profile_index"]),
                "coefficient_candidates": candidate["coefficient_candidates"],
                "score": score,
            }
        if recovered.startswith(expected_prefix) and recovered.endswith("}"):
            best = {
                "seed": seed,
                "coefficient_profile_index": int(candidate["coefficient_profile_index"]),
                "coefficient_candidates": candidate["coefficient_candidates"],
                "score": score,
            }
            break

    if best is None or int(best["score"]) < 100:
        raise SystemExit("Could not recover a plausible brute-force configuration")

    recovered_config = {
        **cfg,
        "marker": "CONFIG_RECOVERED_OK",
        "seed": best["seed"],
        "coefficient_candidates": best["coefficient_candidates"],
        "expected_magic": expected_magic,
        "bruteforce_result": {
            "tested_candidates": tested,
            "coefficient_profile_index": best["coefficient_profile_index"],
            "score": best["score"],
        },
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(recovered_config, indent=2) + "\n", encoding="utf-8")
    Path(args.log).write_text(
        "\n".join(
            [
                "BRUTEFORCE_COMPLETED",
                f"tested_candidates={tested}",
                f"recovered_seed={best['seed']}",
                f"coefficient_profile_index={best['coefficient_profile_index']}",
                f"score={best['score']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print("CONFIG_RECOVERED_OK")


if __name__ == "__main__":
    main()
