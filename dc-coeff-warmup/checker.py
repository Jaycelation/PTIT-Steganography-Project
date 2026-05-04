from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Check submitted answer.")
    parser.add_argument("--answer")
    parser.add_argument("--answer-file")
    parser.add_argument("--expected-file", default="output/private/flag.txt")
    args = parser.parse_args()

    if args.answer_file:
        answer = Path(args.answer_file).read_text(encoding="utf-8").strip()
    elif args.answer:
        answer = args.answer.strip()
    else:
        raise SystemExit("Provide --answer or --answer-file")

    expected = Path(args.expected_file).read_text(encoding="utf-8").strip()
    if answer == expected:
        print("PASS")
    else:
        print("FAIL")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

