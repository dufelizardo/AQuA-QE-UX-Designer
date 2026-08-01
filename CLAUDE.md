# CLAUDE.md

Este arquivo orienta o Claude Code ao trabalhar neste repositório.

## O que é este projeto

Agente que gera UX Specifications (fluxos de navegação por tarefa, arquitetura da informação e recomendações de acessibilidade) a partir de uma Story/Epic do Product Owner e do PRD associado do Product Manager — com rastreabilidade obrigatória à fonte, validação automática e revisão humana no centro do ciclo. Ver `WHITEPAPER.md` (também em inglês: `WHITEPAPER.en.md`) para a visão completa, `docs/agent/` para a especificação completa e `docs/architecture/` para os diagramas (draw.io + SVG).

Este é um **repositório standalone**, próprio, independente de qualquer monorepo — não assuma dependências herdadas de um workspace pai.

**Status atual**: Fase 1 (MVP) implementada — `src/` tem models/skills/workflow/orchestrator/services completos, `run.py` funcional, `tests/` com 92 testes (98% cobertura, tudo mockado).

## Comandos essenciais

```bash
# Instalar/sincronizar dependências
uv sync

# Rodar toda a suíte de testes (mockada, sem chamadas reais a Ollama/Jira/Confluence)
uv run pytest

# Gerar uma UX Specification a partir de uma Story/Epic + PRD
uv run python run.py --jira AQUAQE-10 --confluence <url-do-prd> --saida ux-spec.md

# Ver todas as opções (--refinar, --publicar-confluence, --atualizar-confluence)
uv run python run.py --help
```

Não há configuração própria de lint/type-check (`ruff`/`basedpyright`) neste `pyproject.toml` — isso existe apenas na raiz do monorepo que originou este projeto, não neste repositório standalone.

## Setup local

Ver a seção "Setup"/"Configuração" em `README.md`/`README.pt.md`: requer Python 3.12+, `uv`, Ollama instalado com os modelos `mistral`, `phi4` e `bge-m3` baixados, e um `.env` preenchido a partir de `.env.example`.

## Arquitetura (resumo — detalhe completo em `docs/agent/system_design.md` e `WHITEPAPER.md`)

```
Entrada (Story/Epic via Jira + PRD via Confluence)
  → CLI (run.py) → orchestrator/ux_designer.py → workflow/generate_ux_specification.py → skills/* → models/* → services/*
```

- `src/aqua_qe_ux_designer/models/` — `UXSpecification`, `UserFlow`, `InformationArchitecture`, enum `ArtifactStatus`. Sem `ChatMessage` — este agente não tem skill de chat (`agent_manifest.yaml` só lista `confluence`/`jira` como inputs).
- `src/aqua_qe_ux_designer/skills/` — 17 funções de responsabilidade única (ver `docs/agent/skills.md`).
- `src/aqua_qe_ux_designer/workflow/generate_ux_specification.py` — `generate_ux_specification`, `finalize_ux_specification` (validate→review), `refine_and_finalize_ux_specification`.
- `src/aqua_qe_ux_designer/orchestrator/ux_designer.py` — ponto de entrada único, `handle_request(texto_prd, texto_ticket)`.
- `src/aqua_qe_ux_designer/services/` — integrações externas: `llm_service` (Ollama), `jira_service` (REST API + httpx, **apenas leitura**), `confluence_service` (REST API + httpx, **leitura e escrita** — reaproveitado verbatim do Solution Architect), `embedding_service`/`rag_service` (Ollama `bge-m3` + Qdrant embarcado — memória institucional de refinamento, ver abaixo).

## Convenções críticas

- **Nunca inventar** (GR-UX-1, `docs/agent/guardrails.md`): passo de fluxo ou elemento de arquitetura da informação só existe se rastreável à Story/Epic de entrada.
- **Nunca certificar acessibilidade** (GR-UX-2): `review_accessibility` sempre recomenda verificar um critério WCAG 2.2 específico, nunca afirma conformidade como fato.
- **Nunca fabricar pesquisa/teste com usuário real** (GR-UX-3): a revisão do agente (`review_ux_specification`) é sempre avaliação heurística de especialista (10 Heurísticas de Nielsen), rotulada como tal — o agente não tem acesso a usuários reais nem telemetria de produto.
- **Nunca gerar Personas ou User Journeys** (GR-UX-4, o guardrail mais importante deste agente): esses artefatos já existem no PRD do agente irmão AQuA-QE Product Manager (`synthesize_personas`/`identify_user_journeys`). `extract_ux_context` só lê essas seções como contexto — nenhuma skill deste agente as regenera. Se o PRD não tiver Personas/Journeys, isso é sinalizado como lacuna do PRD, nunca preenchido aqui.
- **User Flow ≠ User Journey**: o Flow deste agente é de nível de navegação concreta (telas exatas de uma tarefa), mais granular que a Journey de negócio/emocional do PM — não é uma duplicata, ver `docs/agent/agent_design.md`.
- **Sem aprovação automática**: nenhuma skill/workflow define `ArtifactStatus.ACCEPTED`. Esse status só é atribuído pelo CLI (`run.py`), após confirmação humana explícita no terminal.
- **Dois LLMs sempre diferentes**: `OLLAMA_MODEL` (padrão `mistral`) gera; `OLLAMA_REVIEW_MODEL` (padrão `phi4`) revisa. Deliberado — mitiga *self-preference bias*.
- **Piloto de provedor via toggle** (`LLM_PROVIDER=ollama|nvidia|cerebras|google|groq`, padrão `ollama`, issue [#2](https://github.com/dufelizardo/AQuA-QE-UX-Designer/issues/2)): implementado depois de necessidade real comprovada — rodadas ao vivo com Ollama local levaram 10-24 minutos cada por competição de CPU. `llm_service.generator_model()`/`reviewer_model()` resolvem o modelo certo conforme o provedor ativo; `complete`/`complete_json` mantêm assinatura inalterada e despacham internamente para Ollama ou um dos quatro provedores em nuvem (todos via SDK `openai` contra endpoint compatível). Modelos padrão (já validados ao vivo nos agentes irmãos antes de portar para cá): NVIDIA `deepseek-ai/deepseek-v4-pro`/`meta/llama-3.3-70b-instruct` (instável em uso real — 503/404/timeout), Cerebras `gpt-oss-120b`/`zai-glm-4.7` (exige billing configurado), Google `gemini-3.1-flash-lite`/`gemini-2.5-flash-lite` (`max_tokens=8192` fixo, rate limit baixo no tier gratuito), Groq `llama-3.3-70b-versatile`/`openai/gpt-oss-120b` (30 req/min, o mais estável em uso real desta plataforma). Não afeta embeddings (`embedding_service.py`/`bge-m3` continuam sempre Ollama, sem toggle).
- **Wireframes/Protótipos/Design System ficam fora** — responsabilidade do futuro agente irmão AQuA-QE UI Designer (ainda não iniciado), que exigirá a primeira integração não-textual da plataforma (Figma). Ver `WHITEPAPER.md`, seção 11.
- **`jira_service` é apenas leitura** — mesmo princípio do Solution Architect; não há hoje um caso de uso real de write-back no Jira a partir de uma UX Specification.
- **`confluence_service` tem escrita gated** — publicar (`--publicar-confluence`, cria página nova, sempre irmã da página de origem do PRD) ou atualizar (`--atualizar-confluence`, edita uma página existente informada) sempre exigem confirmação humana explícita no CLI, mutuamente exclusivos entre si — reaproveita literalmente `get_confluence_publish_location`/`create_confluence_page`/`update_confluence_page` do Solution Architect.
- **Este agente nunca gera PRD** (Product Manager), **nunca gera Épicos/User Stories** (Product Owner), **nunca projeta arquitetura técnica** (Solution Architect). Consome os artefatos já prontos desses três agentes e produz um único artefato novo, a UX Specification.
- **Memória institucional de respostas de refinamento** (`record_refinement_answer`/`suggest_refinement_answer`, `rag_service.py`, issue [#3](https://github.com/dufelizardo/AQuA-QE-UX-Designer/issues/3)): cada resposta que o humano dá num ciclo de refinamento é gravada numa collection Qdrant embarcada própria (`refinement_answer_memory`) via embedding local (`bge-m3`). No ciclo seguinte, se uma pergunta parecida aparecer (mesmo ou outro artefato/projeto), a resposta mais similar já dada é exibida como sugestão no terminal, com o score de similaridade — **nunca aplicada automaticamente**. Sem gate de score mínimo e sem filtro por tipo de artefato. Mesmo padrão já validado ao vivo em PM/PO.
- **Testes sempre mockam** Ollama/Jira/Confluence — nenhum teste em `tests/` deve fazer chamada real de rede, quando a implementação começar.

## Onde procurar mais detalhe

- `docs/agent/` — PRD, System Design, Agent Design, Rules, Guardrails, Persona, Objectives, Skills, Evaluation, Memory (a spec formal completa do agente, escrita antes de qualquer código).
- `knowledge/methodology/` — os frameworks reais que fundamentam os critérios de qualidade (10 Heurísticas de Nielsen, WCAG 2.2, princípios de Arquitetura da Informação, ISO 9241-210, Laws of UX) — nenhum critério do agente foi inventado à parte desses documentos.
- `docs/architecture/` — diagramas visuais (draw.io + SVG) dos mesmos fluxos: arquitetura em camadas, fluxo da UX Specification, GR-UX-4 (Personas/User Journey nunca geradas aqui), ciclo de refinamento humano-no-loop com memória RAG e o pipeline completo com o handoff entre Product Manager, Product Owner, este agente e o futuro UI Designer.
- `WHITEPAPER.md` / `WHITEPAPER.en.md` — visão consolidada, inclui o que foi deliberadamente deixado fora da Fase 1 (seção 11).
