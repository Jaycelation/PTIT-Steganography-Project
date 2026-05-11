from __future__ import annotations

import argparse
import os
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser(description="Check submitted answer.")
    p.add_argument("--answer")
    p.add_argument("--answer-file")
    p.add_argument("--expected-file", default="output/private/flag.txt")
    p.add_argument("--stego", default="output/stego.mp4")
    p.add_argument("--max-bytes", type=int, default=5_000_000)
    args = p.parse_args()
    answer = Path(args.answer_file).read_text(encoding="utf-8").strip() if args.answer_file else (args.answer or "").strip()
    expected = Path(args.expected_file).read_text(encoding="utf-8").strip()
    if answer != expected:
        print("FAIL")
        raise SystemExit(1)
    if Path(args.stego).exists() and os.path.getsize(args.stego) > args.max_bytes:
        print("FAIL")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()

