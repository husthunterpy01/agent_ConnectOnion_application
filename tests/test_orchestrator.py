from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENT_ROOT = PROJECT_ROOT / "my-agent"
sys.path.append(str(AGENT_ROOT))

from research_scholar.orchestrator import ResearchScholarOrchestrator  # noqa: E402
from research_scholar.models import StudentProfile  # noqa: E402


def load_sample_profile() -> StudentProfile:
    profile_path = AGENT_ROOT / "profiles" / "sample_profile.json"
    with profile_path.open() as fh:
        return StudentProfile.from_dict(json.load(fh))


@pytest.mark.parametrize(
    "query, expected_agent_keys",
    [
        (
            "scholarships for women in computer science building social impact startups",
            {"seeker", "matcher", "ranker", "writer", "tracker", "verifier"},
        ),
    ],
)
def test_orchestrator_pipeline(query, expected_agent_keys):
    orchestrator = ResearchScholarOrchestrator()
    profile = load_sample_profile()
    result = orchestrator.run(query=query, profile=profile, limit=3)

    assert set(expected_agent_keys).issubset(result.keys())
    assert result["seeker"]["scholarships"], "Seeker should return scholarships"
    assert len(result["ranker"]["ranked"]) == len(result["matcher"]["eligibility"])
    assert len(result["writer"]["materials"]) > 0


def test_tracker_dates_are_future():
    orchestrator = ResearchScholarOrchestrator()
    profile = load_sample_profile()
    result = orchestrator.run(query="computer science", profile=profile, limit=3)
    for schedule in result["tracker"]["schedules"]:
        assert "milestones" in schedule and schedule["milestones"], "Milestones missing"





