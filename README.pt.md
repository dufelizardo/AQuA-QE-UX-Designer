# AQuA-QE UX Designer

Agente que gera **UX Specifications** — fluxos de navegação por tarefa, arquitetura da informação e recomendações de acessibilidade — a partir de uma Story/Epic já pronta do [AQuA-QE Product Owner](https://github.com/dufelizardo/AQuA-QE-Product-Owner) e do PRD associado do [AQuA-QE Product Manager](https://github.com/dufelizardo/AQuA-QE-Product-Manager). Com rastreabilidade obrigatória à fonte, validação automática e revisão humana no centro do ciclo. Ver `WHITEPAPER.md` para a visão completa.

**Status**: repositório recém-criado — a spec formal (`docs/agent/`) está completa, mas **nenhuma linha de código-fonte foi implementada ainda**. Este README descreve o que o agente **vai** fazer quando a implementação começar, seguindo o mesmo padrão gerar→validar→revisar→aceite humano já usado nos três agentes irmãos.

Este projeto tem repositório git próprio, independente do monorepo raiz (conforme a convenção "todo projeto novo recebe repositório separado" — ver `CLAUDE.md` raiz do workspace).

## O que este agente faz

- Lê uma Story/Epic (Jira) e o PRD associado (Confluence).
- Identifica um Fluxo de Usuário concreto — a sequência de passos/telas para completar a tarefa descrita, rastreável ao requisito de origem.
- Gera uma Arquitetura da Informação para o escopo do Épico.
- Gera recomendações de acessibilidade fundamentadas em WCAG 2.1 — sempre como recomendação a verificar, nunca certificação de conformidade.
- Avalia os fluxos via revisão heurística (10 Heurísticas de Nielsen) — nunca chamada de "teste de usabilidade", já que o agente não tem acesso a usuários reais.
- Roda um ciclo de refinamento humano-no-loop quando a revisão reprova.
- Exporta o resultado em Markdown e, opcionalmente, publica como página irmã do PRD no Confluence.

## O que este agente **não** faz (por design)

- **Nunca gera Personas ou User Journeys** — já são responsabilidade exclusiva do Product Manager (`synthesize_personas`/`identify_user_journeys`, já presentes no PRD). Este agente só as consome como contexto.
- **Nunca gera Wireframes, Protótipos ou Design System** — exige integração real com Figma, que a plataforma ainda não tem. Responsabilidade planejada do futuro agente irmão **AQuA-QE UI Designer** (nome já definido, ainda não iniciado).
- **Nunca conduz pesquisa ou teste de usabilidade com usuários reais** — o agente não tem acesso a usuários reais nem telemetria de produto.
- Nunca gera PRD (Product Manager), Épicos/Stories (Product Owner) ou arquitetura técnica (Solution Architect).

## Arquitetura (resumo — detalhe completo em `docs/agent/system_design.md`)

- **`src/aqua_qe_ux_designer/models/`** (planejado) — `UXSpecification`, `UserFlow`, `InformationArchitecture`, enum `ArtifactStatus`.
- **`src/aqua_qe_ux_designer/skills/`** (planejado) — 13 funções de responsabilidade única (ver `docs/agent/skills.md`).
- **`src/aqua_qe_ux_designer/workflow/`** (planejado) — orquestração da sequência de skills.
- **`src/aqua_qe_ux_designer/orchestrator/`** (planejado) — ponto de entrada único (`handle_request`).
- **`src/aqua_qe_ux_designer/services/`** (planejado) — `llm_service` (Ollama por padrão, sem piloto de provedor em nuvem nesta fase), `jira_service` (apenas leitura), `confluence_service` (leitura + escrita gated, reaproveitado do Solution Architect).

## Configuração

1. Instale [Python 3.12+](https://www.python.org/) e [uv](https://docs.astral.sh/uv/).
2. Instale o [Ollama](https://ollama.com) e baixe os dois modelos locais usados por este agente:
   ```bash
   ollama pull mistral   # geração
   ollama pull phi4      # revisão independente
   ```
3. Instale as dependências:
   ```bash
   uv sync
   ```
4. Copie `.env.example` para `.env` e preencha os valores necessários (o Ollama funciona com os padrões; as credenciais de Jira/Confluence só são necessárias quando a implementação e os comandos reais existirem):
   ```bash
   cp .env.example .env
   ```

## Status detalhado

`docs/agent/` (PRD, System Design, Agent Design, Rules, Guardrails, Persona, Objectives, Skills, Evaluation, Memory) e `docs/standards/` estão completos. `knowledge/methodology/` tem os três documentos reais que fundamentam os critérios de qualidade (10 Heurísticas de Nielsen, WCAG 2.1, princípios de Arquitetura da Informação) — nenhum critério foi inventado à parte deles. `knowledge/templates/ux_specification.md` define o formato de exportação.

Ainda não implementado: `src/` (models/skills/workflow/orchestrator/services), `run.py` (CLI), `tests/`. Ver `WHITEPAPER.md`, seção 12, para os próximos passos de implementação.
