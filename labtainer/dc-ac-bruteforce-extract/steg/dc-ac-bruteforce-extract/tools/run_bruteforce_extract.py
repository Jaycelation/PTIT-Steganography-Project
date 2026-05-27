#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the payload using the recovered brute-force config.")
    parser.add_argument("--input", default="output/stego.mp4")
    parser.add_argument("--config", default="work/recovered_config.json")
    parser.add_argument("--answer", default="work/answer.txt")
    parser.add_argument("--log", default="work/extract.log")
    args = parser.parse_args()

    answer = Path(args.answer)
    answer.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "solve.py",
        "--input",
        args.input,
        "--config",
        args.config,
        "--output",
        str(answer),
    ]
    completed = subprocess.run(cmd, check=True, text=True, capture_output=True)
    recovered = answer.read_text(encoding="utf-8").strip()
    if not recovered:
        raise SystemExit(f"Extractor did not create a non-empty answer file: {answer}")

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    digest = hashlib.sha256(recovered.encode("utf-8")).hexdigest()
    Path(args.log).write_text(
        "\n".join(
            [
                "BRUTEFORCE_EXTRACT_OK",
                f"seed={cfg['seed']}",
                f"coefficient_profile_index={cfg.get('bruteforce_result', {}).get('coefficient_profile_index')}",
                f"stdout={completed.stdout.strip()}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    Path("work/answer_status.txt").write_text("ANSWER_FILE_CREATED\n", encoding="utf-8")
    Path("work/answer.sha256").write_text(digest + "\n", encoding="utf-8")
    Path("work/metrics.json").write_text(
        json.dumps(
            {
                "marker": "METRICS_OK",
                "challenge": "dc-ac-bruteforce-extract",
                "tested_candidates": cfg.get("bruteforce_result", {}).get("tested_candidates"),
                "recovered_seed": cfg["seed"],
                "coefficient_profile_index": cfg.get("bruteforce_result", {}).get("coefficient_profile_index"),
                "answer_sha256": digest,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("BRUTEFORCE_EXTRACT_OK")


if __name__ == "__main__":
    main()
