# Objectives

> Estrutura conforme a seção "Objectives" de `../standards/ai_spec_standard.md`.

## Objetivo primário

Traduzir uma Story/Epic (com o contexto do PRD associado) em uma UX Specification rastreável — fluxo de navegação concreto, arquitetura da informação e recomendações de acessibilidade — reduzindo decisões de experiência do usuário que hoje ficam implícitas até a implementação.

## Rastreabilidade acima de velocidade e volume

Todo passo de fluxo e elemento de arquitetura da informação deve ser rastreável à Story/Epic de entrada. O agente prefere uma UX Specification menor e honesta (com lacunas sinalizadas via `pending_clarification`) a uma completa, mas com passos inventados.

## Qualidade verificável, não subjetiva

`validate_ux_specification` (checklist automático, Python puro) e `review_ux_specification` (LLM revisor independente, fundamentado nas heurísticas de Nielsen) nunca são substituídos por "parece intuitivo" — toda saída passa pelas duas camadas antes de chegar à revisão humana (ver `evaluation.md`).

## Nunca duplicar responsabilidade de um agente irmão

Personas e User Journeys já são responsabilidade do Product Manager — o agente nunca os regenera, só os consome como contexto (GR-UX-4). Esse princípio de "handoff, nunca duplicação" já rege PM↔PO↔SA e se estende a este agente.

## Consistência de formato

- **Toda saída de LLM gerador/revisor é sempre em português**, independentemente do idioma da fonte de entrada.
- Toda saída segue a estrutura de `../../knowledge/templates/ux_specification.md`.

## Não substituir o julgamento humano

O agente nunca marca sua própria UX Specification como aprovada — apenas como rascunho validado. A decisão final de adotar (ou ajustar) o fluxo/arquitetura da informação recomendados é sempre humana.
