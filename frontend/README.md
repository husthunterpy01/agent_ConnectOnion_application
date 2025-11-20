# ResearchScholar Web Dashboard

This Vite + React app renders the JSON output produced by the `ResearchScholarOrchestrator`. Drop in `report.json` from `python agent.py --output report.json` (or load the bundled sample) to visualize:

- Profile summary and goals extracted from the CV parser
- Ranked scholarship opportunities with links and scores
- Inclusive university recommendations + fit reasons
- Deadline notifications generated from the Tracker milestones

## Getting Started

```bash
cd /home/martin/agent_ConnectOnion_application/frontend
npm install          # first run only
npm run dev          # dev server at http://localhost:5173
```

## Usage Tips

- Click **Upload report.json** and select the orchestration output file.
- Use **Load sample data** to preview the UI without running the backend pipeline.
- Upcoming milestones (due within 10 days) surface as alert cards; extend the window inside `src/App.jsx` if needed.

## Build

```bash
npm run build
npm run preview
```

Deploy the contents of `frontend/dist` behind any static host (Netlify, Vercel, Cloudflare Pages, etc.).
