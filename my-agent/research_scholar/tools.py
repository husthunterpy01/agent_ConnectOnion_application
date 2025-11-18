from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any, Dict, List

from .data import load_demo_scholarships
from .models import ApplicationMaterial, ScholarshipOpportunity, StudentProfile

SCHOLARSHIP_DB = load_demo_scholarships()


def _normalize(text: str) -> str:
    return text.lower().strip()


def _deadline_within(deadline: str, within_days: int) -> bool:
    target = datetime.strptime(deadline, "%Y-%m-%d").date()
    return target <= (datetime.utcnow().date() + timedelta(days=within_days))


def seeker_search_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Locate scholarships that mention the query keywords."""
    query = _normalize(payload.get("query", ""))
    limit = payload.get("limit", 10)
    profile = payload.get("profile", {})

    filtered: List[Dict[str, Any]] = []
    query_terms = [_normalize(term) for term in query.split() if term]
    for opp in SCHOLARSHIP_DB:
        corpus = _normalize(f"{opp.title} {opp.description}")
        if query_terms and not any(term in corpus for term in query_terms):
            continue

        if profile:
            location = _normalize(profile.get("location", ""))
            eligible_locations = [_normalize(loc) for loc in opp.eligibility["location"]]
            if "any" not in eligible_locations and location and location not in eligible_locations:
                continue

        filtered.append(opp.to_payload())

    return {"scholarships": filtered[:limit]}


def matcher_filter_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Apply eligibility rules against the student profile."""
    profile = StudentProfile.from_dict(payload["profile"])
    scholarships = [
        ScholarshipOpportunity.from_dict(sch) for sch in payload.get("scholarships", [])
    ]

    eligible: List[Dict[str, Any]] = []
    for opp in scholarships:
        reasons: List[str] = []
        is_match = True

        min_gpa = opp.eligibility.get("min_gpa", 0)
        if profile.gpa < min_gpa:
            is_match = False
            reasons.append(f"GPA {profile.gpa} < required {min_gpa}")

        majors = [m.lower() for m in opp.eligibility.get("majors", [])]
        if majors and profile.major.lower() not in majors:
            is_match = False
            reasons.append("Major not in eligible list")

        citizenships = [c.lower() for c in opp.eligibility.get("citizenship", [])]
        if citizenships and "any" not in citizenships:
            if profile.citizenship.lower() not in citizenships:
                is_match = False
                reasons.append("Citizenship requirement not met")

        demographic_tags = [_normalize(tag) for tag in opp.eligibility.get("demographics", [])]
        if demographic_tags:
            profile_tags = [
                _normalize(v)
                for v in profile.demographics.values()
                if isinstance(v, str)
            ]
            if not any(tag in profile_tags for tag in demographic_tags):
                reasons.append("Demographic preference not matched")

        eligible.append(
            {
                "scholarship": opp.to_payload(),
                "fit_summary": "Strong fit based on GPA/major/location."
                if is_match
                else f"Rejected: {', '.join(reasons) or 'Unknown reason'}",
            }
        )

    return {"eligibility": eligible}


def ranker_score_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Rank scholarships by weighted score (fit, award size, effort, urgency)."""
    ranked: List[Dict[str, Any]] = []
    for item in payload.get("eligibility", []):
        scholarship = ScholarshipOpportunity.from_dict(item["scholarship"])
        fit_penalty = 0 if item["fit_summary"].startswith("Strong") else 20
        amount_score = min(math.ceil(scholarship.amount / 1000), 30)
        effort_map = {"Low": 20, "Medium": 10, "High": 0}
        effort_score = effort_map.get(scholarship.effort_level, 5)
        urgency_bonus = 10 if _deadline_within(scholarship.deadline, 45) else 0
        base = 60 - fit_penalty + amount_score + effort_score + urgency_bonus
        score = max(0, min(100, round(base, 1)))
        ranked.append(
            {
                "scholarship": scholarship.to_payload(),
                "score": score,
                "reasoning": (
                    f"Fit penalty {fit_penalty}, amount {amount_score}, "
                    f"effort {effort_score}, urgency {urgency_bonus}"
                ),
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return {"ranked": ranked}


def writer_materials_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Produce essay outlines, CV bullets, and LOR prompts."""
    profile = StudentProfile.from_dict(payload["profile"])
    materials: List[Dict[str, Any]] = []
    top_n = payload.get("top_n", 3)
    for entry in payload.get("ranked", [])[:top_n]:
        scholarship = ScholarshipOpportunity.from_dict(entry["scholarship"])
        essay_outline = (
            f"1. Hook: {profile.name}'s mission in {profile.major}\n"
            f"2. Impact: Highlight flagship project delivering community impact\n"
            f"3. Alignment: Why {scholarship.sponsor} accelerates the mission\n"
            f"4. Future plan: Milestones funded by ${scholarship.amount}"
        )
        cv_bullets = [
            f"Led {profile.interests[0]} initiative delivering measurable outcomes.",
            "Built open-source tool adopted by 5+ campuses.",
            "Mentored first-gen students on scholarship readiness.",
        ]
        lor_prompt = (
            f"Describe {profile.name}'s leadership in {profile.experiences[0]} "
            "and impact on underrepresented communities."
        )
        materials.append(
            ApplicationMaterial(
                scholarship_id=scholarship.id,
                essay_outline=essay_outline,
                cv_bullets=cv_bullets,
                lor_prompt=lor_prompt,
            ).to_payload()
        )

    return {"materials": materials}


def tracker_schedule_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Generate milestone plan toward each deadline."""
    schedules: List[Dict[str, Any]] = []
    today = datetime.utcnow().date()
    top_n = payload.get("top_n", 3)
    for ranked in payload.get("ranked", [])[:top_n]:
        scholarship = ScholarshipOpportunity.from_dict(ranked["scholarship"])
        deadline = datetime.strptime(scholarship.deadline, "%Y-%m-%d").date()
        milestones = [
            {"label": "Confirm eligibility + requirements", "due": str(deadline - timedelta(days=28))},
            {"label": "Draft essays & CV updates", "due": str(deadline - timedelta(days=21))},
            {"label": "Secure LOR commitments", "due": str(deadline - timedelta(days=14))},
            {"label": "Final review & submit", "due": str(deadline - timedelta(days=3))},
        ]
        schedules.append(
            {
                "scholarship_id": scholarship.id,
                "deadline": scholarship.deadline,
                "starts_in_days": (deadline - today).days,
                "milestones": milestones,
            }
        )

    return {"schedules": schedules}


def verifier_checklist_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that required materials exist for each scholarship."""
    reports: List[Dict[str, Any]] = []
    materials_index = {
        material["scholarship_id"]: material for material in payload.get("materials", [])
    }
    top_n = payload.get("top_n", 3)
    for ranked in payload.get("ranked", [])[:top_n]:
        scholarship = ScholarshipOpportunity.from_dict(ranked["scholarship"])
        material = materials_index.get(scholarship.id, {})
        missing: List[str] = []
        if not material.get("essay_outline"):
            missing.append("Essay outline")
        if not material.get("cv_bullets"):
            missing.append("CV bullets")
        if not material.get("lor_prompt"):
            missing.append("LOR prompt")

        reports.append(
            {
                "scholarship_id": scholarship.id,
                "ready": len(missing) == 0,
                "missing": missing,
                "notes": "Ready for submission." if not missing else "Fill the gaps.",
            }
        )

    return {"qa_reports": reports}

