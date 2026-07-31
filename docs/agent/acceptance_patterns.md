# Acceptance Patterns

> Padrões estruturais que distinguem uma saída aceitável de uma inaceitável, conforme `validation_checklist.md` e `guardrails.md`. Exemplos concretos de domínio (few-shot) ficariam em `knowledge/examples/` — ainda não criado nesta fase.

## Padrão aceitável

Uma UX Specification é aceitável quando:

- Todo passo de `UserFlow` é rastreável a um requisito real da Story/Epic de origem (GR-UX-1).
- `information_architecture` reflete o escopo real do Épico, não uma estrutura genérica de "toda aplicação web".
- Toda recomendação de acessibilidade referencia um critério WCAG 2.1 específico e usa linguagem de recomendação, nunca certificação (GR-UX-2).
- `review_notes` (quando presentes) sempre referenciam a heurística de Nielsen aplicada, nunca alegam pesquisa ou teste com usuário real (GR-UX-3).
- Nenhuma Persona ou User Journey nova aparece na saída — só o que já vem do PRD como contexto (GR-UX-4).
- O campo `status` reflete corretamente o resultado da validação (`draft_validated` ou `pending_clarification`).

## Padrão inaceitável

Uma saída é inaceitável quando apresenta qualquer um dos sinais abaixo:

- **Passo de fluxo inventado** — um passo de navegação sem qualquer menção ou inferência razoável a partir da Story/Epic (viola GR-UX-1).
- **Certificação de acessibilidade** — "este fluxo está em conformidade com WCAG 2.1 AA" apresentado como fato (viola GR-UX-2).
- **Pesquisa/teste fabricado** — "usuários relataram dificuldade neste passo" ou qualquer alegação de observação real (viola GR-UX-3).
- **Persona ou Journey gerada aqui** — mesmo que o PRD não tenha uma, ou tenha uma incompleta (viola GR-UX-4; a lacuna deve ser sinalizada, não preenchida).
- **UX Specification marcada como aprovada** pelo próprio agente, sem passar por revisão humana (viola RULE-UX-5).

## Como usar este documento

Ao avaliar (`evaluation.md`) ou revisar manualmente uma saída do agente, comparar contra os dois padrões acima antes de aceitar a UX Specification como rascunho válido.
