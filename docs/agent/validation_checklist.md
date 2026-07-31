# Validation Checklist

> Checklist aplicado pela skill `validate_ux_specification` antes de qualquer UX Specification ser marcada como `draft_validated` (ver `output_schema.md` e RULE-UX-5 em `rules.md`).

## 1. Rastreabilidade (GR-UX-1)

- [ ] Título e contexto do problema têm origem identificável na fonte de entrada.
- [ ] Nenhum passo de fluxo ou seção de arquitetura da informação foi preenchido por suposição não sinalizada.

## 2. Fluxo de Usuário

- [ ] Há ao menos um `UserFlow`.
- [ ] Cada fluxo tem ao menos 2 passos (um único passo não caracteriza uma sequência de navegação).

## 3. Arquitetura da Informação

- [ ] `information_architecture.sections` não está vazio.

## 4. Acessibilidade (WCAG 2.2, `../../knowledge/methodology/wcag.md`)

- [ ] Há ao menos uma recomendação de acessibilidade.
- [ ] Nenhuma recomendação usa linguagem de certificação ("está em conformidade") — sempre "recomenda-se verificar" (GR-UX-2).

## 5. Nunca duplicar Personas/Journeys (GR-UX-4)

- [ ] A saída não contém uma seção de Personas ou User Journeys gerada por este agente — apenas referência ao que já existe no PRD, se citado como contexto.

## 6. Formato

- [ ] A saída segue a estrutura de `../../knowledge/templates/ux_specification.md`.
