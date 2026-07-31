# CLAUDE.md

Este arquivo orienta o Claude Code ao trabalhar neste repositório.

## O que é este projeto

Agente que gera UX Specifications (fluxos de navegação por tarefa, arquitetura da informação e recomendações de acessibilidade) a partir de uma Story/Epic do Product Owner e do PRD associado do Product Manager — com rastreabilidade obrigatória à fonte, validação automática e revisão humana no centro do ciclo. Ver `WHITEPAPER.md` (também em inglês: `WHITEPAPER.en.md`) para a visão completa.

Este é um **repositório standalone**, próprio, independente de qualquer monorepo — não assuma dependências herdadas de um workspace pai.

**Status atual**: repositório recém-criado (spec formal em `docs/agent/` completa; nenhuma linha de código-fonte implementada ainda — `src/` só tem o stub `__init__.py` do template). Os comandos abaixo refletem o que **vai** existir quando a implementação começar, não o estado atual.

## Comandos essenciais (quando implementado)

```bash
# Instalar/sincronizar dependências
uv sync

# Rodar toda a suíte de testes (mockada, sem chamadas reais a Ollama/Jira/Confluence)
uv run pytest

# Gerar uma UX Specification a partir de uma Story/Epic + PRD
uv run python run.py --jira AQUAQE-10 --confluence <url-do-prd> --saida ux-spec.md

# Ver todas as opções (--refinar, --publicar-confluence)
uv run python run.py --help
```

Não há configuração própria de lint/type-check (`ruff`/`basedpyright`) neste `pyproject.toml` — isso existe apenas na raiz do monorepo que originou este projeto, não neste repositório standalone.

## Setup local

Ver a seção "Setup"/"Configuração" em `README.md`/`README.pt.md`: requer Python 3.12+, `uv`, Ollama instalado com os modelos `mistral` e `phi4` baixados, e um `.env` preenchido a partir de `.env.example`.

## Arquitetura (resumo — detalhe completo em `docs/agent/system_design.md` e `WHITEPAPER.md`)

```
Entrada (Story/Epic via Jira + PRD via Confluence)
  → CLI (run.py) → orchestrator/ux_designer.py → workflow/generate_ux_specification.py → skills/* → models/* → services/*
```

- `src/aqua_qe_ux_designer/models/` (planejado) — `UXSpecification`, `UserFlow`, `InformationArchitecture`, `ChatMessage`, enum `ArtifactStatus`.
- `src/aqua_qe_ux_designer/skills/` (planejado) — 13 funções de responsabilidade única (ver `docs/agent/skills.md`).
- `src/aqua_qe_ux_designer/workflow/generate_ux_specification.py` (planejado) — `generate_ux_specification`, `finalize_ux_specification` (validate→review), `refine_and_finalize_ux_specification`.
- `src/aqua_qe_ux_designer/orchestrator/ux_designer.py` (planejado) — ponto de entrada único, `handle_request(entrada)`.
- `src/aqua_qe_ux_designer/services/` (planejado) — integrações externas: `llm_service` (Ollama), `jira_service` (REST API + httpx, **apenas leitura**), `confluence_service` (REST API + httpx, **leitura e escrita** — reaproveitado do Solution Architect).

## Convenções críticas

- **Nunca inventar** (GR-UX-1, `docs/agent/guardrails.md`): passo de fluxo ou elemento de arquitetura da informação só existe se rastreável à Story/Epic de entrada.
- **Nunca certificar acessibilidade** (GR-UX-2): `review_accessibility` sempre recomenda verificar um critério WCAG 2.1 específico, nunca afirma conformidade como fato.
- **Nunca fabricar pesquisa/teste com usuário real** (GR-UX-3): a revisão do agente (`review_ux_specification`) é sempre avaliação heurística de especialista (10 Heurísticas de Nielsen), rotulada como tal — o agente não tem acesso a usuários reais nem telemetria de produto.
- **Nunca gerar Personas ou User Journeys** (GR-UX-4, o guardrail mais importante deste agente): esses artefatos já existem no PRD do agente irmão AQuA-QE Product Manager (`synthesize_personas`/`identify_user_journeys`). `extract_ux_context` só lê essas seções como contexto — nenhuma skill deste agente as regenera. Se o PRD não tiver Personas/Journeys, isso é sinalizado como lacuna do PRD, nunca preenchido aqui.
- **User Flow ≠ User Journey**: o Flow deste agente é de nível de navegação concreta (telas exatas de uma tarefa), mais granular que a Journey de negócio/emocional do PM — não é uma duplicata, ver `docs/agent/agent_design.md`.
- **Sem aprovação automática**: nenhuma skill/workflow define `ArtifactStatus.ACCEPTED`. Esse status só é atribuído pelo CLI (`run.py`), após confirmação humana explícita no terminal.
- **Dois LLMs sempre diferentes**: `OLLAMA_MODEL` (padrão `mistral`) gera; `OLLAMA_REVIEW_MODEL` (padrão `phi4`) revisa. Deliberado — mitiga *self-preference bias*.
- **Sem piloto de provedor em nuvem nesta fase** (diferente de PM/PO/SA): este agente nasce só com Ollama local. O toggle `LLM_PROVIDER=nvidia|cerebras|google|groq` só é adicionado quando/se surgir necessidade real comprovada (rate limit, instabilidade) — mesmo padrão que motivou sua adição nos três agentes irmãos, nunca construído antecipadamente.
- **Wireframes/Protótipos/Design System ficam fora** — responsabilidade do futuro agente irmão AQuA-QE UI Designer (ainda não iniciado), que exigirá a primeira integração não-textual da plataforma (Figma). Ver `WHITEPAPER.md`, seção 11.
- **`jira_service` é apenas leitura** — mesmo princípio do Solution Architect; não há hoje um caso de uso real de write-back no Jira a partir de uma UX Specification.
- **`confluence_service` tem escrita gated** — publicar (`--publicar-confluence`) sempre exige confirmação humana explícita no CLI e sempre cria a página como irmã da página de origem do PRD — reaproveita literalmente `get_confluence_publish_location`/`create_confluence_page` do Solution Architect.
- **Este agente nunca gera PRD** (Product Manager), **nunca gera Épicos/User Stories** (Product Owner), **nunca projeta arquitetura técnica** (Solution Architect). Consome os artefatos já prontos desses três agentes e produz um único artefato novo, a UX Specification.
- **Testes sempre mockam** Ollama/Jira/Confluence — nenhum teste em `tests/` deve fazer chamada real de rede, quando a implementação começar.

## Onde procurar mais detalhe

- `docs/agent/` — PRD, System Design, Agent Design, Rules, Guardrails, Persona, Objectives, Skills, Evaluation, Memory (a spec formal completa do agente, escrita antes de qualquer código).
- `knowledge/methodology/` — os frameworks reais que fundamentam os critérios de qualidade (10 Heurísticas de Nielsen, WCAG 2.1, princípios de Arquitetura da Informação) — nenhum critério do agente foi inventado à parte desses documentos.
- `WHITEPAPER.md` / `WHITEPAPER.en.md` — visão consolidada, inclui o que foi deliberadamente deixado fora da Fase 1 (seção 11).
