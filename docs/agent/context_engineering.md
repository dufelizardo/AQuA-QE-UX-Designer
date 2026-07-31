# Context Engineering

> Estrutura conforme `../standards/context_engineering_standard.md`.

## Fontes de contexto (Fase 1)

- **`knowledge/methodology/`** — sempre disponível; base para as 10 Heurísticas de Nielsen, WCAG 2.2, princípios de Arquitetura da Informação, ISO 9241-210 e Laws of UX. Pequeno o suficiente para caber direto no prompt de cada skill — sem RAG nesta fase.
- **`knowledge/templates/`** — estrutura de saída (`ux_specification.md`).
- **PRD de origem (via Confluence)** — fonte de Personas/Journeys já existentes, passada como contexto de leitura, nunca regerada (GR-UX-4).
- **Saída de skills anteriores na mesma execução** — ex.: `extract_ux_context` alimenta `identify_user_flows`, que também recebe o texto completo da Story/Epic.

## Fora desta fase

- **`knowledge/domain/`** e `retrieve_chunks` (RAG) — deferidos até o volume de conhecimento exceder o que cabe direto no prompt.
- **Memória de projeto/longo prazo** — ver `memory.md`.

## Orçamento de tokens

- Prioridade de alocação: (1) instruções fixas de persona/regras (`prompt.md`), (2) Story/Epic sendo processada + contexto do PRD, (3) conhecimento de metodologia relevante à skill em execução (ex.: só as 10 Heurísticas de Nielsen para `review_ux_specification`, não todo `knowledge/methodology/`), (4) formato de saída esperado.

## Ordenação no prompt final

1. Persona e objetivos.
2. Regras/guardrails.
3. Conhecimento de metodologia relevante à skill.
4. Story/Epic + contexto do PRD a processar.
5. Formato de saída esperado.

## Atualização/invalidação

Conhecimento de `knowledge/` é reconsultado a cada execução (não cacheado entre sessões diferentes).
