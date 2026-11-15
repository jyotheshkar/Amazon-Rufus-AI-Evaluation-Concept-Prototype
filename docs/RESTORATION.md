# Original application restoration

Restoration date: **15 November 2026**.

## Preserved source

The application returns to the last source revision before the 14 November rebuild:
[`36bd80d3d0376f545bcd16a48212fc7d1b5f6b50`](https://github.com/jyotheshkar/Amazon-Rufus-AI-Evaluation-Concept-Prototype-2026/commit/36bd80d3d0376f545bcd16a48212fc7d1b5f6b50),
dated 11 November 2026.

This preserves the original product retrieval, assistant and judge agents,
adversarial evaluation, SQLite storage, FastAPI endpoints and Next.js dashboard.
The 11 November SDK transport, nonblocking model-call maintenance and patched
frontend dependencies remain part of that baseline.

The separate `web/` static fixture workbench, its checks, and the 14 November
runtime refactor have been removed from the current tree. Earlier commits remain
in Git history. This is a new restoration commit, not a rewritten history.

## Source map

| Component | Location |
| --- | --- |
| Product/index retrieval | `backend/retrieval/` |
| Assistant and judge | `backend/agents/` |
| Evaluation and SQLite persistence | `backend/evaluation/` |
| API endpoints | `backend/main.py`, `backend/routes/` |
| Original dashboard | `frontend/app/`, `frontend/components/` |
| Browser API connection | `frontend/lib/api.ts` |
| Original project brief and phase history | `PROJECT_BRIEF.pdf`, `docs/phase-*.md`, `progress/` |

## Hosting

The existing dashboard is [rufus-eval-engine.vercel.app](https://rufus-eval-engine.vercel.app/).
Its Vercel production deployment was confirmed **READY** on 15 November 2026.

For a deployment from this repository, set the Vercel project root to
`frontend`, use the Next.js framework preset, install with `npm ci` and build
with `npm run build`. Set `NEXT_PUBLIC_API_URL` to the separately hosted
backend's HTTPS URL. It is public browser configuration and must contain no
secret. The Python API's Render configuration remains in `render.yaml`.

The hosted deployment and restored Git source have separate revision histories.
Deployment readiness verifies the frontend build state; it does not establish
API availability, a new backend deployment, live model calls or evaluation
quality.

## Verification

Use the existing checks documented in the README and defined in
`.github/workflows/portfolio-checks.yml`: frontend typecheck, lint, component
tests and build, plus the focused offline agent contracts. These remain distinct
from the full retrieval/evaluation suite, which requires model files and a FAISS
index. The restoration adds no model calls, dataset generation, database migration
or new product feature.
