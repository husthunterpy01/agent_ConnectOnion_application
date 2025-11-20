from __future__ import annotations

from typing import List

from .models import ScholarshipOpportunity, UniversityProgram


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


def load_demo_universities() -> List[UniversityProgram]:
    """Return a small catalog of inclusive university programs."""
    return [
        UniversityProgram(
            id="UNI-001",
            name="Aurora Institute of Technology",
            location="Australia",
            programs=["Computer Science", "Human-Centered AI", "Software Engineering"],
            demographics=["women", "first-generation", "rural"],
            highlights=[
                "Women in Emerging Tech full-ride scholarship",
                "AI for social good research lab with community grants",
                "Mentorship circle for first-generation founders",
            ],
            website="https://example.edu/aurora-tech",
            tuition_support="Full tuition + $10K research stipend",
        ),
        UniversityProgram(
            id="UNI-002",
            name="Pacifica University",
            location="New Zealand",
            programs=["Data Science", "International Relations"],
            demographics=["women", "pacific-islander"],
            highlights=[
                "Leadership incubator for women tackling climate justice",
                "Co-op placements with APAC NGOs",
                "Dedicated funding for first-generation students",
            ],
            website="https://example.edu/pacifica",
            tuition_support="75% tuition waiver + paid co-op",
        ),
        UniversityProgram(
            id="UNI-003",
            name="Global Social Impact College",
            location="Global (Remote)",
            programs=["Product Design", "Public Policy", "AI Ethics"],
            demographics=["any", "first-generation"],
            highlights=[
                "Remote-first bachelor's with community residencies",
                "Scholarships for open-source maintainers",
                "Partner accelerators for social impact startups",
            ],
            website="https://example.edu/gsic",
            tuition_support="Sliding scale + stipend for OSS leaders",
        ),
        UniversityProgram(
            id="UNI-004",
            name="Summit University",
            location="United States",
            programs=["Computer Science", "Entrepreneurship"],
            demographics=["women", "underrepresented-minority"],
            highlights=[
                "Summit Women in Computing Scholars program",
                "Access to venture studio for edtech founders",
                "Global exchange with partner labs in APAC",
            ],
            website="https://example.edu/summit",
            tuition_support="$20K merit award + housing grant",
        ),
    ]

