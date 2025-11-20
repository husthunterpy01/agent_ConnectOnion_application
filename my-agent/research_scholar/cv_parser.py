from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, Dict, List

from connectonion import llm_do
from pydantic import BaseModel, Field, ConfigDict
from .models import StudentProfile


def _load_pdf_reader():
    try:
        module = importlib.import_module("PyPDF2")
        return module.PdfReader
    except ImportError as exc:
        raise ImportError(
            "PyPDF2 is required for PDF text extraction. Install dependencies with "
            "`pip install -r requirements.txt`."
        ) from exc


PdfReader = _load_pdf_reader()

DEFAULT_CV_MODEL = "co/gpt-4o-mini"

CV_SYSTEM_PROMPT = """You are an expert scholarship assistant that converts resume/CV text into a normalized student profile JSON.
Follow these rules strictly:
- Only use facts presented in the CV text. When data is missing, set string fields to "Unknown" (or reasonable defaults like "Undergraduate") and numeric fields to 0.
- GPA must be a 0-4.0 scale float. Use 0 if not provided. Do not hallucinate beyond what's implied.
- Return concise bullet strings for experiences (max 3-4) summarizing the strongest achievements.
- Demographics should include any explicit descriptors (e.g., gender, first-generation, URM). Use key/value pairs; leave empty object if absent.
- Interests and skills must be arrays.
- Goals should capture the candidate's stated mission or career focus in one sentence.
- preferred_countries must list the study destinations or regions explicitly mentioned in the CV (empty list if unspecified).
Your response must validate against the provided Pydantic schema."""


class Demographics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gender: str | None = None
    first_generation: str | None = None
    ethnicity: str | None = None
    socioeconomic_status: str | None = None
    other: str | None = None


class ExtractedProfile(BaseModel):
    name: str = Field(default="Unknown")
    email: str = Field(default="unknown@example.com")
    academic_level: str = Field(default="Unknown")
    gpa: float = Field(default=0.0)
    major: str = Field(default="Undeclared")
    location: str = Field(default="Unknown")
    citizenship: str = Field(default="Unknown")
    interests: List[str] = Field(default_factory=list)
    demographics: Demographics = Field(default_factory=Demographics)
    skills: List[str] = Field(default_factory=list)
    goals: str = Field(default="Unknown")
    experiences: List[str] = Field(default_factory=list)
    preferred_countries: List[str] = Field(default_factory=list)

    def to_student_profile_payload(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "email": self.email,
            "academic_level": self.academic_level,
            "gpa": float(self.gpa),
            "major": self.major,
            "location": self.location,
            "citizenship": self.citizenship,
            "interests": self.interests or [],
            "demographics": {
                key: value
                for key, value in self.demographics.model_dump().items()
                if value not in (None, "")
            },
            "skills": self.skills or [],
            "goals": self.goals,
            "experiences": self.experiences or [],
            "preferred_countries": self.preferred_countries or [],
        }

    def to_student_profile(self):

        return StudentProfile.from_dict(self.to_student_profile_payload())


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    contents: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        contents.append(text.strip())
    return "\n\n".join(filter(None, contents)).strip()


def extract_profile_from_text(cv_text: str, model: str = DEFAULT_CV_MODEL) -> ExtractedProfile:
    if not cv_text.strip():
        raise ValueError("CV text is empty. Unable to extract profile.")

    profile = llm_do(
        cv_text,
        system_prompt=CV_SYSTEM_PROMPT,
        output=ExtractedProfile,
        model=model,
        temperature=0.1,
    )
    return profile


def parse_cv_pdf(pdf_path: Path, model: str = DEFAULT_CV_MODEL) -> ExtractedProfile:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    cv_text = extract_pdf_text(pdf_path)
    return extract_profile_from_text(cv_text, model=model)


def save_profile_json(profile: ExtractedProfile, output_path: Path) -> Path:
    payload = profile.to_student_profile_payload()
    output_path.write_text(profile.model_dump_json(indent=2))
    return output_path


def parse_cv_to_json(pdf_path: Path, output_path: Path, model: str = DEFAULT_CV_MODEL) -> Dict[str, Any]:
    profile = parse_cv_pdf(pdf_path, model=model)
    save_profile_json(profile, output_path)
    return profile.to_student_profile_payload()

