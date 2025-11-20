from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_scholar.cv_parser import DEFAULT_CV_MODEL, parse_cv_to_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a normalized student profile from a CV PDF and save it to JSON."
    )
    parser.add_argument("--pdf", type=Path, required=True, help="Path to the CV PDF file.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("profiles/generated_profile.json"),
        help="Path where the JSON profile should be saved.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_CV_MODEL,
        help="LLM model identifier used for structured extraction.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Parsing CV PDF: {args.pdf}")
    profile_payload = parse_cv_to_json(args.pdf, args.output, model=args.model)

    print(f"Profile saved to {args.output.resolve()}")
    print("=== Extracted Profile ===")
    print(json.dumps(profile_payload, indent=2))


if __name__ == "__main__":
    main()

