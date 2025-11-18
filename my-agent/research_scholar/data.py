from __future__ import annotations

from typing import List

from .models import ScholarshipOpportunity


def load_demo_scholarships() -> List[ScholarshipOpportunity]:
    """Return an in-memory catalog that simulates 3rd-party scholarship APIs."""
    return [
        ScholarshipOpportunity(
            id="RS-001",
            title="Global STEM Innovators Scholarship",
            sponsor="TechForward Foundation",
            amount=15000,
            currency="USD",
            deadline="2025-02-15",
            eligibility={
                "min_gpa": 3.5,
                "majors": ["computer science", "engineering", "data science"],
                "citizenship": ["Any"],
                "location": ["global"],
                "demographics": ["women", "first-generation"],
            },
            effort_level="High",
            description="Supports STEM leaders building tools for social impact.",
            url="https://example.org/scholarships/rs-001",
        ),
        ScholarshipOpportunity(
            id="RS-002",
            title="Asia-Pacific Research Grant",
            sponsor="APAC Scholars",
            amount=8000,
            currency="USD",
            deadline="2025-01-05",
            eligibility={
                "min_gpa": 3.2,
                "majors": ["international relations", "computer science"],
                "citizenship": ["Australia", "New Zealand"],
                "location": ["Australia", "New Zealand"],
                "demographics": [],
            },
            effort_level="Medium",
            description="Funds cross-border research tackling regional challenges.",
            url="https://example.org/scholarships/rs-002",
        ),
        ScholarshipOpportunity(
            id="RS-003",
            title="Open Source Impact Award",
            sponsor="Code4Good",
            amount=5000,
            currency="USD",
            deadline="2024-12-10",
            eligibility={
                "min_gpa": 3.0,
                "majors": ["computer science", "software engineering"],
                "citizenship": ["Any"],
                "location": ["Any"],
                "demographics": [],
            },
            effort_level="Low",
            description="Recognizes students maintaining high-impact OSS projects.",
            url="https://example.org/scholarships/rs-003",
        ),
    ]

