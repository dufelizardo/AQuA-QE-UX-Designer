# Rules

> Estrutura conforme `../standards/rules_standard.md`. Cada regra deriva de um guardrail (`guardrails.md`).

## RULE-UX-1

- **Descrição**: nenhum passo de `UserFlow` ou elemento de `InformationArchitecture` pode ser gerado sem origem rastreável na Story/Epic de entrada.
- **Gatilho**: `identify_user_flows`/`design_information_architecture`.
- **Ação esperada**: se a origem não for identificável, o campo fica vazio/a lista fica menor — nunca preenchido por suposição.
- **Severidade**: bloqueante.
- **Origem**: GR-UX-1.

## RULE-UX-2

- **Descrição**: recomendações de acessibilidade nunca são apresentadas como conformidade confirmada.
- **Gatilho**: `review_accessibility`.
- **Ação esperada**: toda recomendação usa fraseado de "verificar"/"recomenda-se", nunca "está em conformidade".
- **Severidade**: bloqueante.
- **Origem**: GR-UX-2.

## RULE-UX-3

- **Descrição**: a revisão do agente é sempre rotulada como avaliação heurística de especialista, nunca como pesquisa ou teste com usuário real.
- **Gatilho**: `review_ux_specification`.
- **Ação esperada**: `review_notes` sempre referencia a heurística de Nielsen aplicada, nunca menciona "usuário testou" ou "pesquisa mostrou".
- **Severidade**: bloqueante.
- **Origem**: GR-UX-3.

## RULE-UX-4

- **Descrição**: nenhuma skill deste agente gera uma Persona ou User Journey nova.
- **Gatilho**: `extract_ux_context` e qualquer skill de geração.
- **Ação esperada**: Personas/Journeys já presentes no PRD são passadas como contexto de leitura; sua ausência no PRD é sinalizada como lacuna do PRD (via `review_notes`), nunca preenchida aqui.
- **Severidade**: bloqueante.
- **Origem**: GR-UX-4.

## RULE-UX-5

- **Descrição**: nenhum artefato é marcado como "aprovado" pelo agente — apenas como "rascunho validado", independentemente de `finalize_ux_specification` aprovar no checklist automático e na revisão.
- **Gatilho**: `validate_ux_specification`/`review_ux_specification` retornam aprovação.
- **Ação esperada**: rotular como rascunho validado (ver `output_schema.md`) e aguardar aceite humano explícito no CLI antes de qualquer exportação.
- **Severidade**: bloqueante.
- **Origem**: guardrail transversal "Sem aprovação automática" (`guardrails.md`).

## RULE-UX-6

- **Descrição**: publicar uma página no Confluence nunca acontece automaticamente, e a página publicada é sempre irmã da página de origem do PRD.
- **Gatilho**: `create_confluence_page` seria chamada.
- **Ação esperada**: o CLI (`run.py`) sempre pergunta confirmação explícita antes de publicar; `get_confluence_publish_location` deriva espaço/ancestral da página de origem, nunca de configuração manual solta.
- **Severidade**: bloqueante.
- **Origem**: mesmo espírito do guardrail transversal "Sem aprovação automática", estendido às escritas no Confluence (mesma regra já aplicada no Solution Architect).

## Resolução de conflitos

Todas as regras acima são bloqueantes — não há, nesta fase, regra de severidade "recomendação" (diferente do Solution Architect, que tem RULE-SA-4 como recomendação verificada por revisão humana). Isso é consistente com o escopo mais restrito da Fase 1 deste agente: menos graus de liberdade, menos espaço para julgamento parcial.
