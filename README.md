# AQuA-QE UX Designer

An agent that generates **UX Specifications** — task-level navigation flows, information architecture, and accessibility recommendations — from an already-finished Story/Epic from the [AQuA-QE Product Owner](https://github.com/dufelizardo/AQuA-QE-Product-Owner) and the associated PRD from the [AQuA-QE Product Manager](https://github.com/dufelizardo/AQuA-QE-Product-Manager). With mandatory traceability to source, automatic validation, and human review at the center of the cycle. See `WHITEPAPER.en.md` for the full picture.

**Status**: freshly created repository — the formal spec (`docs/agent/`) is complete, but **no source code has been implemented yet**. This README describes what the agent **will** do once implementation begins, following the same generate→validate→review→human-accept pattern already used by the three sibling agents.

This project has its own git repository, independent from the root monorepo (per the "every new project gets its own repository" convention — see the root `CLAUDE.md`).

## What this agent does

- Reads a Story/Epic (Jira) and the associated PRD (Confluence).
- Identifies a concrete User Flow — the sequence of steps/screens to complete the described task, traceable to the source requirement.
- Generates an Information Architecture for the Epic's scope.
- Generates accessibility recommendations grounded in WCAG 2.1 — always as a recommendation to verify, never a compliance certification.
- Evaluates flows via heuristic review (Nielsen's 10 Heuristics) — never called "usability testing," since the agent has no access to real users.
- Runs a human-in-the-loop refinement cycle when review rejects the output.
- Exports the result as Markdown and, optionally, publishes it as a sibling page of the PRD on Confluence.

## What this agent does **not** do (by design)

- **Never generates Personas or User Journeys** — these are already the exclusive responsibility of the Product Manager (`synthesize_personas`/`identify_user_journeys`, already present in the PRD). This agent only consumes them as context.
- **Never generates Wireframes, Prototypes, or a Design System** — that requires real Figma integration, which the platform doesn't have yet. Planned responsibility of a future sibling agent, **AQuA-QE UI Designer** (name already defined, not yet started).
- **Never conducts research or usability testing with real users** — the agent has no access to real users or product telemetry.
- Never generates a PRD (Product Manager), Epics/Stories (Product Owner), or technical architecture (Solution Architect).

## Architecture (summary — full detail in `docs/agent/system_design.md`)

- **`src/aqua_qe_ux_designer/models/`** (planned) — `UXSpecification`, `UserFlow`, `InformationArchitecture`, `ArtifactStatus` enum.
- **`src/aqua_qe_ux_designer/skills/`** (planned) — 13 single-responsibility functions (see `docs/agent/skills.md`).
- **`src/aqua_qe_ux_designer/workflow/`** (planned) — orchestrates the skill sequence.
- **`src/aqua_qe_ux_designer/orchestrator/`** (planned) — single entry point (`handle_request`).
- **`src/aqua_qe_ux_designer/services/`** (planned) — `llm_service` (Ollama by default, no cloud provider pilot at this phase), `jira_service` (read-only), `confluence_service` (read + gated write, reused from Solution Architect).

## Setup

1. Install [Python 3.12+](https://www.python.org/) and [uv](https://docs.astral.sh/uv/).
2. Install [Ollama](https://ollama.com) and pull the two local models this agent uses:
   ```bash
   ollama pull mistral   # generation
   ollama pull phi4      # independent review
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Copy `.env.example` to `.env` and fill in the values you need (Ollama works with the defaults; Jira/Confluence credentials will only be needed once real commands exist):
   ```bash
   cp .env.example .env
   ```

## Detailed status

`docs/agent/` (PRD, System Design, Agent Design, Rules, Guardrails, Persona, Objectives, Skills, Evaluation, Memory) and `docs/standards/` are complete. `knowledge/methodology/` has the three real documents grounding the quality criteria (Nielsen's 10 Heuristics, WCAG 2.1, Information Architecture principles) — no criterion was invented apart from them. `knowledge/templates/ux_specification.md` defines the export format.

Not yet implemented: `src/` (models/skills/workflow/orchestrator/services), `run.py` (CLI), `tests/`. See `WHITEPAPER.en.md`, section 12, for the next implementation steps.
