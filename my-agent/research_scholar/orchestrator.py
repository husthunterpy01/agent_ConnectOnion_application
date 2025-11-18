from __future__ import annotations

from typing import Any, Dict

from .agents import (
    build_matcher_agent,
    build_ranker_agent,
    build_seeker_agent,
    build_tracker_agent,
    build_verifier_agent,
    build_writer_agent,
    DEFAULT_MODEL,
)
from .models import StudentProfile
from .tools import (
    matcher_filter_tool,
    ranker_score_tool,
    seeker_search_tool,
    tracker_schedule_tool,
    verifier_checklist_tool,
    writer_materials_tool,
)


class ResearchScholarOrchestrator:
    """Coordinates the multi-agent workflow end-to-end."""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self.model = model
        # ConnectOnion Agent handles (for future conversational extensions)
        self.seeker_agent = build_seeker_agent(model)
        self.matcher_agent = build_matcher_agent(model)
        self.ranker_agent = build_ranker_agent(model)
        self.writer_agent = build_writer_agent(model)
        self.tracker_agent = build_tracker_agent(model)
        self.verifier_agent = build_verifier_agent(model)

    def run(self, query: str, profile: StudentProfile, limit: int = 5) -> Dict[str, Any]:
        seeker_payload = {
            "query": query,
            "limit": limit,
            "profile": profile.to_payload(),
        }
        seeker_result = seeker_search_tool(seeker_payload)

        matcher_payload = {
            "profile": profile.to_payload(),
            "scholarships": seeker_result["scholarships"],
        }
        matcher_result = matcher_filter_tool(matcher_payload)

        ranker_result = ranker_score_tool(matcher_result)

        writer_payload = {
            "profile": profile.to_payload(),
            "ranked": ranker_result["ranked"],
            "top_n": 3,
        }
        materials_result = writer_materials_tool(writer_payload)

        tracker_payload = {"ranked": ranker_result["ranked"], "top_n": 3}
        tracker_result = tracker_schedule_tool(tracker_payload)

        verifier_payload = {
            "ranked": ranker_result["ranked"],
            "materials": materials_result["materials"],
            "top_n": 3,
        }
        verifier_result = verifier_checklist_tool(verifier_payload)

        return {
            "query": query,
            "profile": profile.to_payload(),
            "seeker": seeker_result,
            "matcher": matcher_result,
            "ranker": ranker_result,
            "writer": materials_result,
            "tracker": tracker_result,
            "verifier": verifier_result,
        }

