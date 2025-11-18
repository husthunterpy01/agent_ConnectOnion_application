# ResearchScholar AI  
**An Autonomous Scholarship Research Lab Built with ConnectOnion**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![ConnectOnion](https://img.shields.io/badge/Framework-ConnectOnion-7B4DFF)

> **Find. Match. Apply. Win.**  
> Your 24/7 AI-powered scholarship co-pilot — built for students, by AI.

---

## Overview

**ResearchScholar** is a **multi-agent AI system** built using the **[ConnectOnion framework](https://docs.connectonion.com)** that automates the entire scholarship application lifecycle:

1. **Discovers** global scholarships from 1000+ sources  
2. **Matches** them to your academic & personal profile  
3. **Ranks** by success probability and effort/reward  
4. **Writes** tailored essays, CV mappings, and LOR prompts  
5. **Tracks** deadlines and application status  

No more endless searching. Just results.

---

## Architecture (Multi-Agent Swarm)

### Agent Hierarchy
```
User
  ↓
Orchestrator (Central Coordinator)
  ├── Seeker (Scholarship Discovery)
  ├── Matcher (Eligibility Matching)
  ├── Ranker (Priority Scoring)
  ├── Writer (Application Materials)
  ├── Tracker (Deadline Management)
  └── Verifier (Quality Assurance)
```

```mermaid
graph TD
    A[User] --> B[Orchestrator]
    B --> C[Seeker]
    B --> D[Matcher]
    B --> E[Ranker]
    B --> F[Writer]
    B --> G[Tracker]
    B --> H[Verifier]
```

### Agent Descriptions

**Orchestrator**
- Central coordinator managing all agents
- Routes requests and aggregates results
- Maintains conversation state
- Handles error recovery

**Seeker**
- Searches scholarship databases and APIs
- Web scraping from university sites
- Monitors new opportunities
- Data sources: Fastweb, Scholarships.com, College Board

**Matcher**
- Compares student profile with eligibility criteria
- Filters by GPA, major, demographics, location
- Applies rule-based matching logic
- Reads from student profile database

**Ranker**
- Calculates fit scores (0-100%)
- Estimates success probability
- Considers award amount vs application effort (ROI)
- Uses ML models for prediction

**Writer**
- Generates personalized essay drafts
- Creates CV bullet points
- Suggests letter of recommendation prompts
- Uses templates and student experiences

**Tracker**
- Monitors application deadlines
- Sends timely reminders
- Tracks submission status
- Calendar integration

**Verifier**
- Validates application completeness
- Checks requirement fulfillment
- Quality assurance before submission
- Ensures no missing documents

### Data Flow
```
User Query
    ↓
Orchestrator receives request
    ↓
Orchestrator → Seeker → [Scholarship APIs + Web Sources]
    ↓
Seeker returns scholarship list
    ↓
Orchestrator → Matcher → [Student Profile DB + Rules Engine]
    ↓
Matcher returns eligible scholarships
    ↓
Orchestrator → Ranker → [ML Scoring Model]
    ↓
Ranker returns prioritized list
    ↓
Orchestrator → User with ranked results
```

---

## Quick Start

1. **Install dependencies**
   ```bash
   cd /home/martin/agent_ConnectOnion_application
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configure API keys**
   - Copy `.env.example` to `.env` inside `my-agent/` (or create it manually).
   - Add either `OPENONION_API_KEY=co/XXXX` or your `OPENAI_API_KEY=sk-XXXX`.
3. **Run the ResearchScholar agent**
   ```bash
   cd my-agent
   python agent.py \
     --profile profiles/sample_profile.json \
     --query "scholarships for women in computer science building social impact startups"
   ```
4. **Optional**: save structured output
   ```bash
   python agent.py --output report.json
   ```

---

## Repository Layout

```
agent_ConnectOnion_application/
├── README.md               # Product brief & architecture
├── requirements.txt        # Python dependencies
├── my-agent/               # ConnectOnion implementation
│   ├── agent.py            # CLI entry point
│   ├── profiles/           # Sample student profiles
│   └── research_scholar/   # Core package (models, tools, orchestrator)
└── tests/                  # Pytest suite validating the pipeline
```

---

## Feature Coverage vs README

| Requirement                               | Implementation Detail                              |
|-------------------------------------------|----------------------------------------------------|
| Multi-agent swarm (Seeker→Verifier)       | `research_scholar.tools` + `research_scholar.agents`|
| Orchestrator that routes between agents   | `ResearchScholarOrchestrator.run()`                |
| Scholarship discovery & matching pipeline | `seeker_search_tool`, `matcher_filter_tool`        |
| Ranking by probability & effort           | `ranker_score_tool` scoring heuristic              |
| Application material drafting             | `writer_materials_tool`                            |
| Deadline tracking & reminders             | `tracker_schedule_tool`                            |
| QA / completeness verification            | `verifier_checklist_tool`                          |

---

## Testing

Run the automated checks anytime you modify the pipeline:

```bash
pytest
```

The suite validates that every stage (Seeker→Verifier) returns structured data for the provided reference profile.

---

## Extending the System

- **Swap in real data sources**: Implement adapters in `research_scholar/data.py` that fetch from APIs (Fastweb, College Board, etc.) and inject them into the seeker tool.
- **Plug in ML rankers**: Replace `ranker_score_tool` with a model-backed scoring service; expose weight overrides via CLI flags.
- **Calendar/webhook integration**: Extend `tracker_schedule_tool` to push reminders to Google Calendar, Slack, or email.
- **Conversation layer**: Use the instantiated ConnectOnion `Agent` objects in `research_scholar/agents.py` to hold stateful chats with students for profile enrichment.

---
