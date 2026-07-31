# AQuA-QE UX Designer — Whitepaper

## 1. Resumo executivo

O AQuA-QE UX Designer é o quarto agente da plataforma AQuA-QE, especializado em traduzir requisitos funcionais já detalhados (Story/Epic do Product Owner, com o contexto do PRD do Product Manager) em fluxos de navegação concretos, arquitetura da informação e recomendações de acessibilidade. Ele responde a uma pergunta que nenhum dos três agentes irmãos responde: **como o usuário vai efetivamente interagir com a solução para completar uma tarefa específica?**

Este documento descreve a Fase 1 do agente — deliberadamente mais enxuta do que a especialidade completa de um UX Designer humano, porque metade do que pareceriam especialidades exclusivas (Personas, User Journey) já são responsabilidade do Product Manager, e outra parte (Wireframes, Protótipos, Design System) exige uma integração (Figma) que a plataforma ainda não tem — reservada para um futuro agente irmão, o AQuA-QE UI Designer.

**Status no momento deste documento**: a spec formal (`docs/agent/`) está completa; a implementação (`src/`, `run.py`, `tests/`) ainda não começou.

## 2. Fundamentação metodológica

Nenhum critério de qualidade deste agente foi inventado. Cada um é documentado em `knowledge/methodology/` e referenciado diretamente pelas skills e guardrails do agente:

- **10 Heurísticas de Usabilidade de Nielsen** (`nielsen_heuristics.md`) — fundamenta a revisão heurística dos fluxos (`review_ux_specification`).
- **WCAG 2.1** (`wcag.md`) — fundamenta as recomendações de acessibilidade (`review_accessibility`).
- **Princípios de Arquitetura da Informação** (`information_architecture.md`, Rosenfeld & Morville) — fundamenta `design_information_architecture`.

## 3. Princípios de design (guardrails)

O mesmo princípio central dos três agentes irmãos se aplica aqui: quando a revisão aponta um problema, o agente não tenta se autocorrigir adivinhando a resposta certa — ele interrompe e pergunta a um humano. Ver `docs/agent/guardrails.md` para o detalhe formal (GR-UX-1 a GR-UX-4).

O guardrail mais importante e mais específico deste agente é **GR-UX-4 — nunca gerar Personas ou User Journeys**: esses artefatos já existem no PRD do Product Manager. Um "UX Designer" que os regenerasse criaria duas fontes divergentes do mesmo conceito — o mesmo tipo de risco que motivou o Product Owner nunca regerar um PRD depois que o Product Manager passou a existir.

Igualmente importante é **GR-UX-3 — nunca fabricar pesquisa ou teste com usuário real**: o agente não tem acesso a usuários reais nem telemetria de produto. A especialidade "Teste de Usabilidade" do papel humano de UX Designer é reformulada aqui como revisão heurística de especialista (Nielsen), sempre rotulada como tal.

## 4. Arquitetura

```
Story/Epic (Jira) + PRD (Confluence)
  → CLI (run.py) → orchestrator/ux_designer.py → workflow/generate_ux_specification.py → skills/* → models/* → services/*
```

Um pipeline de skills orquestrado sequencialmente, com dois pontos de checagem antes de qualquer saída ser considerada válida: validação automática (checklist estrutural, Python puro) e revisão humana obrigatória. Ver `docs/agent/system_design.md` para o fluxo de dados completo.

## 5. As 13 skills (planejadas)

Skills sem LLM (Python puro, determinística):

- `validate_ux_specification` — checklist estrutural, retorna motivos específicos de reprovação (não `bool`).
- `format_ux_specification_markdown` — formata a UX Specification em Markdown.

Skills com LLM gerador (`OLLAMA_MODEL`, padrão `mistral`):

- `extract_ux_context`, `identify_user_flows`, `design_information_architecture`, `review_accessibility`, `generate_ux_clarifying_questions`, `refine_ux_specification`.

Skills com LLM revisor independente (`OLLAMA_REVIEW_MODEL`, padrão `phi4` — deliberadamente um modelo diferente do gerador, para mitigar *self-preference bias*):

- `review_ux_specification` — fundamentada nas 10 Heurísticas de Nielsen.

Skills de I/O externo:

- `read_jira_issue` (leitura, Jira Cloud REST API), `read_confluence_page` (leitura, Confluence Cloud REST API), `get_confluence_publish_location`/`create_confluence_page` (escrita gated no Confluence, reaproveitados do Solution Architect).

Detalhamento completo de entrada/saída/erros de cada skill em `docs/agent/skills.md`.

## 6. O ciclo de refinamento interativo (herdado de PM/PO/SA)

1. Uma UX Specification chega reprovada com `review_notes` preenchido de uma de duas formas: `validate_ux_specification` reprova o checklist automático e grava os motivos específicos — sem gastar uma chamada de LLM revisor; ou, se o checklist passa, `review_ux_specification` reprova com apontamentos heurísticos concretos (ex.: "o fluxo de confirmação viola a Heurística 1 — visibilidade do status do sistema").
2. `generate_ux_clarifying_questions` transforma cada apontamento em uma pergunta objetiva e acionável.
3. O CLI (`run.py --refinar`) apresenta as perguntas no terminal; **um humano real responde**.
4. `refine_ux_specification` reescreve os campos afetados usando as respostas como contexto real — preservando o texto/nível de detalhe dos campos que as respostas não abordam (mesmo cuidado aplicado desde o início nos três agentes irmãos, aprendido com um bug real).

## 7. O handoff no ecossistema AQuA-QE

```
Product Manager
      │
      ▼
     PRD
      │
   ┌──┴──┐
   ▼     ▼
  PO    UX Designer
   │     │
   ▼     ▼
Backlog  UX Specification
   │     │
   └──┬──┘
      ▼
Solution Architect
```

O UX Designer consome o PRD (para contexto de Personas/Journeys já existentes) e o Backlog do PO (Stories/Epics, para os requisitos concretos a partir dos quais os fluxos são derivados). O Solution Architect, quando processar o mesmo PRD/Backlog, pode consultar a UX Specification como referência adicional de como a solução deve suportar a interação do usuário — mas essa integração (SA lendo UX Specification) não está implementada nesta fase; é uma extensão natural a considerar quando houver demanda real.

## 8. Modos de operação

Um único fluxo nesta fase — gerar a UX Specification a partir de uma Story/Epic e do PRD associado. Sem `--modo` (mesma razão de design do Solution Architect: só existe um artefato nesta fase).

## 9. Stack técnico

- **LLM local via Ollama (único provedor nesta fase)** — `mistral` para geração, `phi4` como revisor independente. Diferente de PM/PO/SA, **este agente não nasce com o piloto de provedor em nuvem** (`LLM_PROVIDER=nvidia|cerebras|google|groq`) — esse toggle só foi adicionado nos agentes irmãos depois de necessidade real comprovada (rate limit, instabilidade); aqui, é adicionado quando/se a mesma necessidade surgir, não construído antecipadamente.
- **`uv`** para dependências — projeto standalone (repositório próprio, fora do monorepo que o originou).
- **Sem RAG/embeddings nesta fase** — `knowledge/methodology/` tem só 3 arquivos, pequeno o suficiente para caber direto no prompt de cada skill.

## 10. Qualidade e cobertura de testes

Ainda não implementado — quando a implementação começar, seguirá o mesmo padrão dos três agentes irmãos: testes sempre mockam Ollama/Jira/Confluence, nenhuma chamada real de rede, avaliação em três camadas (checklist automático, LLM-como-juiz, revisão humana — ver `docs/agent/evaluation.md`).

## 11. O que ainda falta (deliberadamente adiado, não esquecido)

- **Personas e User Journeys** — permanentemente fora de escopo deste agente (não uma questão de fase): já são responsabilidade do Product Manager. Gerá-los aqui também criaria duas fontes divergentes do mesmo artefato.
- **Pesquisa com usuário real e Teste de Usabilidade real** — permanentemente fora de escopo: o agente não tem acesso a usuários reais nem telemetria de produto (Hotjar, Google Analytics, Mixpanel, Amplitude, Maze). Substituídos por revisão heurística de especialista, nunca apresentada como pesquisa/teste real.
- **Wireframes, Protótipos e Design System** — adiado para um agente irmão futuro, o **AQuA-QE UI Designer** (nome já definido, escopo ainda não formalizado). Requer a primeira integração não-textual da plataforma (Figma real, leitura e escrita).
- **Piloto de provedor de LLM em nuvem** — adiado até haver necessidade real comprovada, mesmo padrão que motivou sua adoção em PM/PO/SA.
- **Memória institucional de respostas de refinamento (RAG)** — já implementada nos agentes irmãos Product Manager e Product Owner; cotada como oportunidade a considerar desde o dia 1 da implementação deste agente, mas não incluída na Fase 1 por padrão (ver `docs/agent/memory.md`).
- **Integração SA↔UX Designer** (Solution Architect consumindo a UX Specification como contexto adicional) — não implementada nesta fase, extensão natural a considerar quando houver demanda real.

## 12. Como executar

Ainda não aplicável — ver "Status detalhado" em `README.md`/`README.pt.md` para o que já existe (spec formal completa) e o que falta (implementação de `src/`, `run.py`, `tests/`). Quando a implementação começar, seguirá a mesma sequência das dos agentes irmãos: models → skills → workflow → orchestrator → `run.py`, com testes desde o início.

## 13. Conclusão

O AQuA-QE UX Designer fecha uma lacuna real da plataforma — a camada de experiência do usuário entre "o que construir" (backlog do PO) e "como construir tecnicamente" (Solution Design do SA) — sem duplicar responsabilidades já cobertas pelos agentes irmãos. Sua Fase 1 é deliberadamente mais restrita do que a especialidade completa de UX Design, seguindo o mesmo princípio que já rege toda a plataforma: entregar o núcleo que cabe no padrão estabelecido (rastreabilidade, validação, revisão humana, artefato textual) primeiro, e documentar honestamente o que foi adiado — não construí-lo especulativamente.
