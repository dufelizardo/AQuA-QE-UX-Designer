# Output Schema

> Estrutura de dados retornada por `generate_ux_specification` e exportada por `format_ux_specification_markdown`, alinhada a `../../knowledge/templates/ux_specification.md`. Implementada como dataclasses reais em `../../src/aqua_qe_ux_designer/models/` (`UXSpecification`, `UserFlow`, `InformationArchitecture`) — o JSON abaixo é a representação conceitual.

## Schema da UX Specification

```
{
  "id": "<string, ex.: UX-001>",
  "title": "<string — extraído por extract_ux_context>",
  "context_problem": "<string — resumo do problema/tarefa, extraído da fonte>",
  "user_flows": [
    {
      "name": "<nome da tarefa, ex.: Agendamento assistido presencial>",
      "steps": ["<passo em ordem, evidenciado/inferível do texto — nunca inventado (GR-UX-1)>"],
      "source_reference": "<trecho da Story/Epic de origem>"
    }
  ],
  "information_architecture": {
    "sections": ["<seção/categoria de navegação, evidenciada/inferível do texto>"],
    "navigation_notes": "<string — como as seções se relacionam>",
    "source_reference": "<trecho da fonte>"
  },
  "accessibility_recommendations": [
    "<recomendação fundamentada em WCAG 2.2, sempre como 'a verificar', nunca certificação — GR-UX-2>"
  ],
  "source_reference": "<texto de origem completo (Story/Epic + contexto do PRD), para rastreabilidade — GR-UX-1>",
  "prd_reference": "<URL/ID da página Confluence do PRD de origem, conforme informado em --confluence>",
  "ticket_reference": "<chave do ticket Jira de origem, conforme informado em --jira>",
  "personas_reference": "<trecho de Personas citado literalmente do PRD por extract_ux_context — nunca gerado; vazio se o PRD não tiver essa seção (GR-UX-4), o que reprova o checklist e aciona o ciclo de esclarecimento>",
  "journey_reference": "<trecho de User Journey citado literalmente do PRD por extract_ux_context — nunca gerado; vazio se o PRD não tiver essa seção (GR-UX-4), o que reprova o checklist e aciona o ciclo de esclarecimento>",
  "recommendations_synthesis": ["<síntese priorizada gerada por synthesize_recommendations, combinando accessibility_recommendations e review_notes — nunca um item que não esteja em uma das duas>"],
  "status": "draft_validated | pending_clarification | accepted",
  "review_notes": ["<motivo de reprovação do checklist (validate_ux_specification) OU apontamento heurístico do revisor (review_ux_specification), se houver — sempre rotulado como avaliação de especialista, nunca teste real (GR-UX-3)>"]
}
```

## Valores válidos de `status`

- **`draft_validated`** — passou no checklist automático (`validation_checklist.md`) e na revisão por LLM (`review_ux_specification`); ainda não tem aceitação humana (ver RULE-UX-5 em `rules.md`).
- **`pending_clarification`** — o agente interrompeu por ambiguidade/incompletude na fonte, ou o revisor reprovou a UX Specification; use o par `generate_ux_clarifying_questions`/`refine_ux_specification` para endereçar os apontamentos.
- **`accepted`** — setado **apenas** pelo CLI (`run.py`), nunca pela lógica automática do agente, após confirmação explícita do usuário.

## Formato de exportação (`format_ux_specification_markdown`)

A saída em Markdown segue diretamente a estrutura de `../../knowledge/templates/ux_specification.md`, preenchida a partir deste schema.
