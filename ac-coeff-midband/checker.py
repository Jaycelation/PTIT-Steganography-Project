from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Check submitted answer.")
    parser.add_argument("--answer")
    parser.add_argument("--answer-file")
    parser.add_argument("--expected-file", default="output/private/flag.txt")
    args = parser.parse_args()

    answer = Path(args.answer_file).read_text(encoding="utf-8").strip() if args.answer_file else (args.answer or "").strip()
    expected = Path(args.expected_file).read_text(encoding="utf-8").strip()
    if answer == expected:
        print("PASS")
    else:
        print("FAIL")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

