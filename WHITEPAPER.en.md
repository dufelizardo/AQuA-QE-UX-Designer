# AQuA-QE UX Designer — Whitepaper

## 1. Executive summary

AQuA-QE UX Designer is the platform's fourth agent, specialized in translating already-detailed functional requirements (a Story/Epic from the Product Owner, with context from the Product Manager's PRD) into concrete navigation flows, information architecture, and accessibility recommendations. It answers a question none of the three sibling agents answer: **how will the user actually interact with the solution to complete a specific task?**

This document describes Phase 1 of the agent — deliberately leaner than a human UX Designer's full specialty set, because half of what would look like exclusive UX specialties (Personas, User Journey) are already the Product Manager's responsibility, and another part (Wireframes, Prototypes, Design System) requires an integration (Figma) the platform doesn't have yet — reserved for a future sibling agent, AQuA-QE UI Designer.

**Status as of this document**: the formal spec (`docs/agent/`) is complete; implementation (`src/`, `run.py`, `tests/` — 78 tests, 99% coverage) is done (Phase 1/MVP).

## 2. Methodological grounding

No quality criterion used by this agent was invented. Each one is documented in `knowledge/methodology/` and referenced directly by the agent's skills and guardrails:

- **Nielsen's 10 Usability Heuristics** (`nielsen_heuristics.md`) — grounds the heuristic review of flows (`review_ux_specification`).
- **WCAG 2.2** (`wcag.md`) — grounds accessibility recommendations (`review_accessibility`).
- **Information Architecture principles** (`information_architecture.md`, Rosenfeld & Morville) — grounds `design_information_architecture`.
- **Laws of UX** (`laws_of_ux.md`, Jon Yablonski) — Hick's/Jakob's/Miller's Law and Cognitive Load, more concrete and operationalizable than Nielsen's Heuristics; ground `identify_user_flows`/`design_information_architecture` and complement `review_ux_specification`.
- **ISO 9241-210** (`iso_9241_210.md`) — doesn't ground a single skill, but formally justifies why the whole agent follows an iterative generate→validate→review→refine→human-accept cycle instead of producing the UX Specification in one shot (see `docs/agent/agent_design.md`, item 8).

## 3. Design principles (guardrails)

The same core principle from the three sibling agents applies here: when review flags a problem, the agent doesn't try to self-correct by guessing the right answer — it stops and asks a human. See `docs/agent/guardrails.md` for the formal detail (GR-UX-1 through GR-UX-4).

The most important and most specific guardrail here is **GR-UX-4 — never generate Personas or User Journeys**: these artifacts already exist in the Product Manager's PRD. A "UX Designer" that regenerated them would create two diverging sources of the same concept — the same kind of risk that led Product Owner to never regenerate a PRD once Product Manager existed.

Equally important is **GR-UX-3 — never fabricate research or testing with real users**: the agent has no access to real users or product telemetry. The "Usability Testing" specialty from the human UX Designer role is reframed here as expert heuristic review (Nielsen), always labeled as such.

## 4. Architecture

```
Story/Epic (Jira) + PRD (Confluence)
  → CLI (run.py) → orchestrator/ux_designer.py → workflow/generate_ux_specification.py → skills/* → models/* → services/*
```

A sequentially orchestrated pipeline of skills, with two checkpoints before any output is considered valid: automatic validation (structural checklist, pure Python) and mandatory human review. See `docs/agent/system_design.md` for the full data flow.

## 5. The 15 skills

Skills with no LLM (pure Python, deterministic):

- `validate_ux_specification` — structural checklist, returns specific rejection reasons (not a `bool`).
- `format_ux_specification_markdown` — formats the UX Specification as Markdown.

Skills with generator LLM (`OLLAMA_MODEL`, default `mistral`):

- `extract_ux_context`, `identify_user_flows`, `design_information_architecture`, `review_accessibility`, `generate_ux_clarifying_questions`, `refine_ux_specification`, `synthesize_recommendations`.

Skills with independent reviewer LLM (`OLLAMA_REVIEW_MODEL`, default `phi4` — deliberately a different model from the generator, to mitigate *self-preference bias*):

- `review_ux_specification` — grounded in Nielsen's 10 Usability Heuristics and the Laws of UX.

External I/O skills:

- `read_jira_issue` (read, Jira Cloud REST API), `read_confluence_page` (read, Confluence Cloud REST API), `get_confluence_publish_location`/`create_confluence_page`/`update_confluence_page` (gated write to Confluence, reused from Solution Architect).

Full input/output/error detail for each skill is in `docs/agent/skills.md`.

## 6. The interactive refinement cycle (inherited from PM/PO/SA)

1. A UX Specification arrives rejected with `review_notes` populated one of two ways: `validate_ux_specification` rejects the automatic checklist and records the specific reasons — without spending an LLM reviewer call; or, if the checklist passes, `review_ux_specification` rejects with concrete heuristic findings (e.g., "the confirmation flow violates Heuristic 1 — visibility of system status").
2. `generate_ux_clarifying_questions` turns each finding into a direct, actionable question.
3. The CLI (`run.py --refinar`) presents the questions in the terminal; **a real human answers**.
4. `refine_ux_specification` rewrites the affected fields using the answers as real context — preserving the text/level of detail of fields the answers don't address (the same care applied from the start in the three sibling agents, learned from a real bug).

## 7. The handoff in the AQuA-QE ecosystem

```
Product Manager
      │
      ▼
     PRD
      │
   ┌──┴──┐
   ▼     ▼
  PO    UX Designer
   │     │
   ▼     ▼
Backlog  UX Specification
   │     │
   └──┬──┘
      ▼
Solution Architect
```

UX Designer consumes the PRD (for context on already-existing Personas/Journeys) and the PO's Backlog (Stories/Epics, for the concrete requirements flows are derived from). Solution Architect, when processing the same PRD/Backlog, could consult the UX Specification as additional reference for how the solution should support user interaction — but that integration (SA reading UX Specification) isn't implemented at this phase; it's a natural extension to consider once real demand exists.

## 8. Modes of operation

A single flow at this phase — generate the UX Specification from a Story/Epic and its associated PRD. No `--modo` (same design reasoning as Solution Architect: only one artifact exists at this phase).

## 9. Technical stack

- **Local LLM via Ollama (sole provider at this phase)** — `mistral` for generation, `phi4` as independent reviewer. Unlike PM/PO/SA, **this agent is not born with the cloud provider pilot** (`LLM_PROVIDER=nvidia|cerebras|google|groq`) — that toggle was only added to the sibling agents after real, proven need (rate limits, instability); here, it's added when/if the same need arises, not built ahead of time.
- **`uv`** for dependencies — standalone project (own repository, outside the monorepo that originated it).
- **No RAG/embeddings at this phase** — `knowledge/methodology/` has only 5 files, small enough to fit directly in each skill's prompt.

## 10. Quality and test coverage

78 tests, 99% coverage — same pattern as the three sibling agents: tests always mock Ollama/Jira/Confluence, no real network calls, three-layer evaluation (automatic checklist, LLM-as-judge, human review — see `docs/agent/evaluation.md`).

## 11. What's still missing (deliberately deferred, not forgotten)

- **Personas and User Journeys** — permanently out of scope for this agent (not a phasing question): already the Product Manager's responsibility. Generating them here too would create two diverging sources of the same artifact.
- **Research with real users and real Usability Testing** — permanently out of scope: the agent has no access to real users or product telemetry (Hotjar, Google Analytics, Mixpanel, Amplitude, Maze). Replaced by expert heuristic review, never presented as real research/testing.
- **Wireframes, Prototypes, and Design System** — deferred to a future sibling agent, **AQuA-QE UI Designer** (name already defined, scope not yet formalized). Requires the platform's first non-text integration (real Figma, read and write).
- **Cloud LLM provider pilot** — deferred until real, proven need exists, same pattern that motivated its adoption in PM/PO/SA.
- **Institutional memory of refinement answers (RAG)** — already implemented in the sibling Product Manager and Product Owner agents; flagged as an opportunity to consider from day 1 of this agent's implementation, but not included in Phase 1 by default (see `docs/agent/memory.md`).
- **SA↔UX Designer integration** (Solution Architect consuming the UX Specification as additional context) — not implemented at this phase, a natural extension to consider once real demand exists.

## 12. How to run

```bash
uv sync
uv run pytest
uv run python run.py --jira AQUAQE-10 --confluence <prd-url> --saida ux-spec.md
```

See `README.md`/`README.pt.md` for full setup (Ollama, `.env`) and `run.py --help` for all options (`--refinar`, `--publicar-confluence`).

## 13. Conclusion

AQuA-QE UX Designer closes a real gap in the platform — the user-experience layer between "what to build" (PO's backlog) and "how to build it technically" (SA's Solution Design) — without duplicating responsibilities already covered by the sibling agents. Its Phase 1 is deliberately narrower than the full UX Design specialty, following the same principle that already governs the whole platform: ship the core that fits the established pattern (traceability, validation, human review, text artifact) first, and honestly document what was deferred — never build it speculatively.
