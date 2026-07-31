# Template — UX Specification (UXS)

> Estrutura padrão, sem conteúdo de domínio. Ver `../../docs/agent/output_schema.md` para o schema de dados exato gerado pelo agente (`UXSpecification`, seções 4-6 abaixo). As seções 3, 7-9 e 11 **não são geradas por este agente** — existem no template para que o documento final leia como uma UX Specification completa, mas seu conteúdo é sempre referência a outro artefato ou um placeholder explícito de fase futura, nunca um artefato novo criado aqui (GR-UX-4, `docs/agent/agent_design.md`).

## 1. Objetivo

`<a tarefa/problema que motiva este fluxo, herdado da Story/Epic + PRD — gerado por extract_ux_context>`

## 2. Escopo

`<link/ID da página Confluence do PRD de origem + chave do ticket Jira (Epic/Story) de origem — não um resumo do texto completo, só a referência>`

## 3. Personas

> **Não gerado por este agente.** Referência direta às Personas já existentes no PRD do Product Manager (`synthesize_personas`) — este documento nunca cria uma Persona nova (GR-UX-4). Se o PRD não tiver Personas, esta seção fica marcada "não disponível no PRD de origem" e o checklist automático (`validate_ux_specification`) reprova a UX Specification até que o ciclo de esclarecimento humano-no-loop informe quem são os usuários.

`<trecho de Personas citado literalmente do PRD de origem>`

## 4. User Flows

`<lista de UserFlow — nome, passos em ordem, origem rastreável — gerado por identify_user_flows>`

## 5. Information Architecture

`<seções/categorias de navegação e como se relacionam — gerado por design_information_architecture>`

## 6. Recomendações de Acessibilidade

`<lista de recomendações fundamentadas em WCAG 2.2, sempre "a verificar", nunca certificação — gerado por review_accessibility>`

## 7. User Journey

> **Não gerado por este agente.** Referência direta à User Journey já existente no PRD do Product Manager (`identify_user_journeys`) — mesma razão da seção 3, inclusive a reprovação automática se ausente. A Journey do PM é de nível de negócio/emocional; os User Flows (seção 4) deste agente são de nível de navegação concreta para a tarefa específica, não um substituto.

`<trecho de User Journey citado literalmente do PRD de origem>`

## 8. Wireframes

> **Fora de escopo nesta fase.** Gerar wireframes exige integração com uma ferramenta de design visual (Figma), que a plataforma ainda não tem. Esta seção existe para manter a estrutura completa do documento; responsabilidade planejada do futuro agente irmão AQuA-QE UI Designer (nome definido, escopo ainda não formalizado — ver `WHITEPAPER.md`, seção 11). Quando existir, o link para o(s) wireframe(s) no Figma correspondente(s) a este User Flow apareceria aqui.

## 9. Protótipos

> **Fora de escopo nesta fase**, mesma razão da seção 8 — protótipos interativos dependem dos wireframes existirem primeiro.

## 10. Regras de Usabilidade

`<apontamentos da revisão heurística, fundamentados nas 10 Heurísticas de Nielsen e nas Laws of UX — gerado por review_ux_specification, sempre rotulado como avaliação de especialista, nunca teste com usuário real (GR-UX-3). Cada apontamento é uma string única; quando tem um tópico identificável, o tópico aparece em destaque antes do restante do texto.>`

## 11. Design System

> **Fora de escopo nesta fase**, mesma razão da seção 8 — contribuições de Design System (novos componentes/variações) dependem de Wireframes/Protótipos existirem primeiro.

## 12. Recomendações

`<síntese curta apontando para as recomendações de acessibilidade (seção 6) e usabilidade (seção 10) já listadas acima — não repete o conteúdo completo dessas seções, só refere a contagem de itens, para o time de desenvolvimento/design revisar antes da implementação>`

## Rastreabilidade

`<tabela de/para: cada artefato gerado (PRD de origem, Story/Epic de origem, cada User Flow, Information Architecture) ligado ao trecho de origem que o fundamenta — não um dump do texto completo da fonte, ver GR-UX-1>`

## Relação com a hierarquia de artefatos

```
PRD (Product Manager)
 ├── Personas (seção 3, referenciada aqui)
 └── User Journey (seção 7, referenciada aqui)
      │
      ▼
Épico / User Story (Product Owner)
      │
      ▼
UX Specification (UX Designer) — seções 1, 2, 4, 5, 6, 10, 12 geradas aqui
      │
      ▼
Wireframes / Protótipos / Design System (futuro UI Designer — seções 8, 9, 11, fora de escopo nesta fase)
```

A UX Specification não substitui o PRD nem a Story — é a ponte entre "o que construir" (requisito funcional) e "como o usuário interage com isso" (fluxo de navegação), explicitando decisões de experiência que hoje ficam implícitas até a implementação. O Solution Architect pode consultar esta UX Specification como referência adicional ao desenhar a arquitetura técnica (fluxos de navegação ajudam a definir componentes/APIs/limites entre módulos), mas não depende dela — mesmo PRD/Backlog seguem sendo suas entradas principais.
