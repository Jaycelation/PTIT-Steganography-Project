#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the public brute-force config.")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--output", default="work/config_audit.txt")
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    brute = cfg.get("bruteforce", {})
    if cfg.get("challenge") != "dc-ac-bruteforce":
        raise SystemExit("Unexpected challenge name in public config")
    forbidden = [name for name in ("seed", "coefficient_profile") if name in cfg]
    if forbidden:
        raise SystemExit("Public config leaks hidden brute-force fields: " + ", ".join(forbidden))

    seed_min = int(brute["seed_min"])
    seed_max = int(brute["seed_max"])
    profiles = brute["coefficient_profiles"]
    if seed_min > seed_max:
        raise SystemExit("Invalid seed range")
    if not profiles:
        raise SystemExit("No coefficient profile candidates found")

    total = (seed_max - seed_min + 1) * len(profiles)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                "CONFIG_AUDIT_OK",
                f"seed_min={seed_min}",
                f"seed_max={seed_max}",
                f"coefficient_profiles={len(profiles)}",
                f"ac_step={cfg['ac_step']}",
                f"total_candidates={total}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print("CONFIG_AUDIT_OK")


if __name__ == "__main__":
    main()
