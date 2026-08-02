# AQuA-QE UX Designer

An agent that generates **UX Specifications** — task-level navigation flows, information architecture, and accessibility recommendations — from an already-finished Story/Epic from the [AQuA-QE Product Owner](https://github.com/dufelizardo/AQuA-QE-Product-Owner) and the associated PRD from the [AQuA-QE Product Manager](https://github.com/dufelizardo/AQuA-QE-Product-Manager). With mandatory traceability to source, automatic validation, and human review at the center of the cycle. See `WHITEPAPER.en.md` for the full picture.

**What problem it solves**: turns an accepted Story/Epic + its PRD into a concrete UX Specification, instead of diagramming flows by hand.
**Who uses it**: UX designers who need a grounded starting draft (navigation flow, information architecture, accessibility notes) before their own design work.
**What's the benefit**: every flow step traceable to the source requirement, accessibility grounded in WCAG 2.2, Personas/Journeys never re-invented (always cited from the PRD) — never two diverging sources of the same artifact.
**How it works (high level)**: Story/Epic + PRD → User Flow + Information Architecture → accessibility recommendations → validate → review (Nielsen's heuristics) → [refine] → human accepts.

## Example

**Input**: a Story/Epic (Jira) + the associated PRD (Confluence).

**Output** — a real UX Specification generated live this way ("Agendamento Assistido Presencial"), with these sections:

```
1. Objetivo          5. Information Architecture   9. Protótipos
2. Escopo            6. Recomendações de           10. Regras de Usabilidade
3. Personas             Acessibilidade              11. Design System
4. User Flows        7. User Journey                12. Recomendações
                      8. Wireframes                  Rastreabilidade
```

**Status**: Phase 1 (MVP) implemented, following the same generate→validate→review→human-accept pattern already used by the three sibling agents.

This project has its own git repository, independent from the root monorepo (per the "every new project gets its own repository" convention — see the root `CLAUDE.md`).

## What this agent does

- Reads a Story/Epic (Jira) and the associated PRD (Confluence).
- Identifies a concrete User Flow — the sequence of steps/screens to complete the described task, traceable to the source requirement.
- Generates an Information Architecture for the Epic's scope.
- Generates accessibility recommendations grounded in WCAG 2.2 — always as a recommendation to verify, never a compliance certification.
- Evaluates flows via heuristic review (Nielsen's 10 Heuristics) — never called "usability testing," since the agent has no access to real users.
- Runs a human-in-the-loop refinement cycle when review rejects the output.
- Exports the result as Markdown and, optionally, publishes it as a sibling page of the PRD on Confluence or updates an existing page.

## What this agent does **not** do (by design)

- **Never generates Personas or User Journeys** — these are already the exclusive responsibility of the Product Manager (`synthesize_personas`/`identify_user_journeys`, already present in the PRD). This agent only consumes them as context.
- **Never generates Wireframes, Prototypes, or a Design System** — that requires real Figma integration, which the platform doesn't have yet. Planned responsibility of a future sibling agent, **AQuA-QE UI Designer** (name already defined, not yet started).
- **Never conducts research or usability testing with real users** — the agent has no access to real users or product telemetry.
- Never generates a PRD (Product Manager), Epics/Stories (Product Owner), or technical architecture (Solution Architect).

## Architecture (summary — full detail in `docs/agent/system_design.md`)

- **`src/aqua_qe_ux_designer/models/`** — `UXSpecification`, `UserFlow`, `InformationArchitecture`, `ArtifactStatus` enum.
- **`src/aqua_qe_ux_designer/skills/`** — 17 single-responsibility functions (see `docs/agent/skills.md`).
- **`src/aqua_qe_ux_designer/workflow/`** — orchestrates the skill sequence.
- **`src/aqua_qe_ux_designer/orchestrator/`** — single entry point (`handle_request`).
- **`src/aqua_qe_ux_designer/services/`** — `llm_service` (Ollama by default, plus a cloud provider toggle — `LLM_PROVIDER=nvidia|cerebras|google|groq`), `jira_service` (read-only), `confluence_service` (read + gated write, reused from Solution Architect), `embedding_service`/`rag_service` (Ollama `bge-m3` + embedded Qdrant — institutional refinement memory).

## Setup

1. Install [Python 3.12+](https://www.python.org/) and [uv](https://docs.astral.sh/uv/).
2. Install [Ollama](https://ollama.com) and pull the three local models this agent uses:
   ```bash
   ollama pull mistral   # generation
   ollama pull phi4      # independent review
   ollama pull bge-m3    # embeddings (institutional refinement memory)
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Copy `.env.example` to `.env` and fill in the values you need (Ollama works with the defaults; Jira/Confluence credentials are needed for `--jira`/`--confluence`/`--publicar-confluence`):
   ```bash
   cp .env.example .env
   ```

## Detailed status

`docs/agent/` (PRD, System Design, Agent Design, Rules, Guardrails, Persona, Objectives, Skills, Evaluation, Memory) and `docs/standards/` are complete. `knowledge/methodology/` has the five real documents grounding the quality criteria (Nielsen's 10 Heuristics, WCAG 2.2, Information Architecture principles, ISO 9241-210, Laws of UX) — no criterion was invented apart from them. `knowledge/templates/ux_specification.md` defines the export format (12 sections, including PRD references and explicit future-phase placeholders).

`src/` (models/skills/workflow/orchestrator/services), `run.py` (CLI), and `tests/` (92 tests, 98% coverage) are implemented. See `WHITEPAPER.en.md`, section 11, for what's deliberately left out of this phase.

---

**Eduardo Felizardo Cândido**
Senior QA Automation Engineer | AI-driven Testing | Robot Framework & Python
