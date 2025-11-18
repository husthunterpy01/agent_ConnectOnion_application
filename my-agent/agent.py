"""
ResearchScholar AI - Multi-Agent Scholarship Assistant built with ConnectOnion.

Run `python agent.py --profile profiles/sample_profile.json --query "..."`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from research_scholar.models import StudentProfile
from research_scholar.orchestrator import ResearchScholarOrchestrator


def load_profile(profile_path: Path) -> StudentProfile:
    with profile_path.open() as fh:
        data: Dict[str, Any] = json.load(fh)
    return StudentProfile.from_dict(data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the ResearchScholar pipeline.")
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("profiles/sample_profile.json"),
        help="Path to a JSON file containing the student profile.",
    )
    parser.add_argument(
        "--query",
        type=str,
        required=False,
        default="scholarships for women in computer science building social impact startups",
        help="Discovery query sent to the Seeker agent.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of scholarships returned from the Seeker agent.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to save the JSON report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = load_profile(args.profile)
    orchestrator = ResearchScholarOrchestrator()
    result = orchestrator.run(query=args.query, profile=profile, limit=args.limit)

    print("=== ResearchScholar Report ===")
    print(json.dumps(result, indent=2))

    if args.output:
        args.output.write_text(json.dumps(result, indent=2))
        print(f"\nReport saved to {args.output.resolve()}")


if __name__ == "__main__":
    main()
