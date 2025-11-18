# ResearchScholar Agent (`my-agent/`)

This package hosts the production-ready implementation of the ResearchScholar multi-agent swarm described in the root `README.md`.

## Components

- `agent.py` – CLI entry point; wires args → orchestrator → JSON report.
- `research_scholar/` – Core package with datamodels, data adapters, tools, agent builders, and orchestrator.
- `profiles/` – Sample student profiles for quick demos.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
cp .env.example .env   # create if missing; add API key
```

## Running the pipeline

```bash
python agent.py \
  --profile profiles/sample_profile.json \
  --query "scholarships for women in computer science building social impact startups" \
  --output report.json
```

The command prints the structured swarm report and (optionally) writes it to disk.

## Customizing

- **Profiles**: Drop additional JSON files in `profiles/` and point `--profile` to them.
- **Seeker data sources**: Replace the mock catalog in `research_scholar/data.py` with API fetchers or database queries.
- **Ranking logic**: Tune weights or plug in ML models in `research_scholar/tools.py::ranker_score_tool`.
- **Notification hooks**: Extend `tracker_schedule_tool` to emit Slack/Email/webhook reminders tied to each milestone.

## Testing

From the repo root:

```bash
pytest tests/test_orchestrator.py
```

The suite ensures the orchestration path (Seeker→Verifier) returns all expected payloads for the reference student profile.
