# Evaluation

> Estrutura conforme `../standards/evaluation_standard.md`. Decisão de produto: avaliação combina checklist automático, revisão por um segundo LLM e revisão humana obrigatória (nenhum substitui o outro).

## Métricas

- **Taxa de aprovação automática** — % de UX Specifications geradas que passam no checklist (`validation_checklist.md`) sem interrupção por ambiguidade.
- **Taxa de aceitação sem retrabalho** — % de UX Specifications em `draft_validated` aceitas pelo designer/PO sem edição substancial (métrica de sucesso do PRD).
- **Cobertura de rastreabilidade** — % de passos de fluxo com `source_reference` preenchido a partir da fonte real, não vazio.
- **Taxa de recomendações de acessibilidade fundamentadas** — % de recomendações que citam um critério WCAG 2.1 específico, não genérico.

## Casos de teste

- **Caminho feliz** — Story clara, com critérios de aceitação detalhados; deve gerar uma UX Specification `draft_validated` sem interrupção.
- **Story sem critérios de aceitação suficientes** — `identify_user_flows` deve gerar um fluxo mais curto ou `validate_ux_specification` deve reprovar, nunca inventar passos para "completar" o fluxo (GR-UX-1).
- **PRD sem Personas/Journeys** — o agente nunca preenche essa lacuna gerando uma Persona/Journey própria; a ausência é sinalizada em `review_notes` (GR-UX-4).
- **Recomendação de acessibilidade sem critério WCAG citado** — deve ser rejeitada/sinalizada como genérica demais (GR-UX-2).
- **`review_notes` mencionando "usuário testou" ou "pesquisa mostrou"** — nunca deveria ocorrer; se ocorrer, é uma falha de prompt a corrigir imediatamente (GR-UX-3).

## Método de avaliação

1. **Checklist automático** (`validate_ux_specification`) — roda em toda execução, aplicando `validation_checklist.md`. Sem LLM.
2. **LLM-como-juiz** (`review_ux_specification`) — roda após o checklist automático aprovar; usa um modelo diferente do gerador (`OLLAMA_REVIEW_MODEL`, padrão `phi4`, enquanto as skills de geração usam `mistral`) para evitar self-preference bias. Avalia os fluxos contra as 10 Heurísticas de Nielsen; os problemas apontados ficam em `UXSpecification.review_notes`, sempre rotulados como avaliação heurística.
3. **Revisão humana obrigatória** — toda UX Specification `draft_validated` passa por aceite humano explícito antes de ser exportada; feedback da revisão alimenta a métrica de taxa de aceitação.

## Frequência

- Casos de teste automatizados rodam a cada mudança em prompt, regras ou skills que possam afetar comportamento (ver `prompt.md`, `rules.md`).
- Métricas de aceitação humana são agregadas continuamente a partir do uso real do agente.

## Critério de aprovação de uma nova versão do agente

Uma nova versão do prompt/regras/skills só substitui a anterior se não piorar a taxa de aceitação sem retrabalho nem a taxa de aprovação automática nos casos de teste de regressão.

## Registro de regressões

Toda falha encontrada em uso real (ex.: passo de fluxo inventado aceito, recomendação de acessibilidade sem critério citado, review_notes alegando teste real) vira um novo caso de teste permanente nesta lista.
