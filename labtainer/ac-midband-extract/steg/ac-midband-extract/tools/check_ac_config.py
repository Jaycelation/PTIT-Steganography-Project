#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate public AC midband extraction config.")
    parser.add_argument("--config", default="output/public_config.json")
    parser.add_argument("--hint", default="output/hint.txt")
    parser.add_argument("--output", default="work/ac_config.txt")
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    coeffs = cfg.get("coefficient_candidates", [])
    if not coeffs:
        raise SystemExit("No AC coefficient candidates in public config.")
    if not cfg.get("flag_length_bytes") or not cfg.get("seed"):
        raise SystemExit("Public config is missing seed or flag length.")

    hint = Path(args.hint).read_text(encoding="utf-8").strip() if Path(args.hint).exists() else ""
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                "AC_CONFIG_OK",
                f"seed={cfg['seed']}",
                f"flag_length_bytes={cfg['flag_length_bytes']}",
                f"q_step={cfg['q_step']}",
                f"coefficient_candidates={coeffs}",
                f"hint={hint}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print("AC_CONFIG_OK")


if __name__ == "__main__":
    main()
