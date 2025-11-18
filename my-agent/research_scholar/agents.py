from __future__ import annotations

from connectonion import Agent

from .tools import (
    matcher_filter_tool,
    ranker_score_tool,
    seeker_search_tool,
    tracker_schedule_tool,
    verifier_checklist_tool,
    writer_materials_tool,
)

DEFAULT_MODEL = "co/gpt-4o-mini"


def build_agent(name: str, system_prompt: str, tool, model: str = DEFAULT_MODEL) -> Agent:
    return Agent(
        name=name,
        system_prompt=system_prompt,
        tools=[tool],
        model=model,
    )


def build_seeker_agent(model: str = DEFAULT_MODEL) -> Agent:
    return build_agent(
        "scholarship-seeker",
        "Locate scholarships that match the query and call the search tool.",
        seeker_search_tool,
        model,
    )


def build_matcher_agent(model: str = DEFAULT_MODEL) -> Agent:
    return build_agent(
        "scholarship-matcher",
        "Compare student profile to eligibility criteria and explain fits.",
        matcher_filter_tool,
        model,
    )


def build_ranker_agent(model: str = DEFAULT_MODEL) -> Agent:
    return build_agent(
        "scholarship-ranker",
        "Score scholarships by fit, award amount, effort, and urgency.",
        ranker_score_tool,
        model,
    )


def build_writer_agent(model: str = DEFAULT_MODEL) -> Agent:
    return build_agent(
        "scholarship-writer",
        "Draft essays, CV bullets, and LOR prompts for each scholarship.",
        writer_materials_tool,
        model,
    )


def build_tracker_agent(model: str = DEFAULT_MODEL) -> Agent:
    return build_agent(
        "scholarship-tracker",
        "Produce milestone schedules and reminders for deadlines.",
        tracker_schedule_tool,
        model,
    )


def build_verifier_agent(model: str = DEFAULT_MODEL) -> Agent:
    return build_agent(
        "scholarship-verifier",
        "Validate application packets and highlight missing artifacts.",
        verifier_checklist_tool,
        model,
    )

