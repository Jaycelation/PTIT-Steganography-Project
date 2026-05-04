from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser(description="Check submitted answer.")
    p.add_argument("--answer")
    p.add_argument("--answer-file")
    p.add_argument("--expected-file", default="output/private/flag.txt")
    args = p.parse_args()
    answer = Path(args.answer_file).read_text(encoding="utf-8").strip() if args.answer_file else (args.answer or "").strip()
    expected = Path(args.expected_file).read_text(encoding="utf-8").strip()
    if answer == expected:
        print("PASS")
    else:
        print("FAIL")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

