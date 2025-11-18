from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class StudentProfile:
    name: str
    email: str
    academic_level: str
    gpa: float
    major: str
    location: str
    citizenship: str
    interests: List[str]
    demographics: Dict[str, Any]
    skills: List[str]
    goals: str
    experiences: List[str]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "StudentProfile":
        return StudentProfile(**data)

    def to_payload(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScholarshipOpportunity:
    id: str
    title: str
    sponsor: str
    amount: int
    currency: str
    deadline: str
    eligibility: Dict[str, Any]
    effort_level: str
    description: str
    url: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ScholarshipOpportunity":
        return ScholarshipOpportunity(**data)

    def to_payload(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ApplicationMaterial:
    scholarship_id: str
    essay_outline: str
    cv_bullets: List[str]
    lor_prompt: str

    def to_payload(self) -> Dict[str, Any]:
        return asdict(self)

