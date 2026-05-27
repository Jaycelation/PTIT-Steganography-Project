#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the bounded seed/coefficient-profile candidate space.")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--output", default="work/candidates.json")
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    brute = cfg["bruteforce"]
    seed_min = int(brute["seed_min"])
    seed_max = int(brute["seed_max"])
    profiles = brute["coefficient_profiles"]
    candidates = [
        {"seed": seed, "coefficient_profile_index": idx, "coefficient_candidates": profile}
        for seed in range(seed_min, seed_max + 1)
        for idx, profile in enumerate(profiles)
    ]

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "marker": "CANDIDATE_SPACE_OK",
                "seed_min": seed_min,
                "seed_max": seed_max,
                "coefficient_profiles": profiles,
                "total_candidates": len(candidates),
                "candidates": candidates,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("CANDIDATE_SPACE_OK")


if __name__ == "__main__":
    main()
