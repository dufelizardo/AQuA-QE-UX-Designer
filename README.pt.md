# AQuA-QE UX Designer

Agente que gera **UX Specifications** — fluxos de navegação por tarefa, arquitetura da informação e recomendações de acessibilidade — a partir de uma Story/Epic já pronta do [AQuA-QE Product Owner](https://github.com/dufelizardo/AQuA-QE-Product-Owner) e do PRD associado do [AQuA-QE Product Manager](https://github.com/dufelizardo/AQuA-QE-Product-Manager). Com rastreabilidade obrigatória à fonte, validação automática e revisão humana no centro do ciclo. Ver `WHITEPAPER.md` para a visão completa.

**Qual problema resolve**: transforma uma Story/Epic aceita + a PRD associada numa UX Specification concreta, em vez de diagramar fluxos manualmente.
**Quem usa**: UX designers que precisam de um rascunho fundamentado (fluxo de navegação, arquitetura da informação, notas de acessibilidade) antes do próprio trabalho de design.
**Qual o benefício**: cada passo do fluxo rastreável ao requisito de origem, acessibilidade fundamentada em WCAG 2.2, Personas/Jornadas nunca reinventadas (sempre citadas da PRD) — nunca duas fontes divergentes do mesmo artefato.
**Como funciona (alto nível)**: Story/Epic + PRD → User Flow + Arquitetura da Informação → recomendações de acessibilidade → valida → revisa (heurísticas de Nielsen) → [refina] → aceite humano.

**Status**: Fase 1 (MVP) implementada, seguindo o mesmo padrão gerar→validar→revisar→aceite humano já usado nos três agentes irmãos.

Este projeto tem repositório git próprio, independente do monorepo raiz (conforme a convenção "todo projeto novo recebe repositório separado" — ver `CLAUDE.md` raiz do workspace).

## O que este agente faz

- Lê uma Story/Epic (Jira) e o PRD associado (Confluence).
- Identifica um Fluxo de Usuário concreto — a sequência de passos/telas para completar a tarefa descrita, rastreável ao requisito de origem.
- Gera uma Arquitetura da Informação para o escopo do Épico.
- Gera recomendações de acessibilidade fundamentadas em WCAG 2.2 — sempre como recomendação a verificar, nunca certificação de conformidade.
- Avalia os fluxos via revisão heurística (10 Heurísticas de Nielsen) — nunca chamada de "teste de usabilidade", já que o agente não tem acesso a usuários reais.
- Roda um ciclo de refinamento humano-no-loop quando a revisão reprova.
- Exporta o resultado em Markdown e, opcionalmente, publica como página irmã do PRD no Confluence ou atualiza uma página já existente.

## O que este agente **não** faz (por design)

- **Nunca gera Personas ou User Journeys** — já são responsabilidade exclusiva do Product Manager (`synthesize_personas`/`identify_user_journeys`, já presentes no PRD). Este agente só as consome como contexto.
- **Nunca gera Wireframes, Protótipos ou Design System** — exige integração real com Figma, que a plataforma ainda não tem. Responsabilidade planejada do futuro agente irmão **AQuA-QE UI Designer** (nome já definido, ainda não iniciado).
- **Nunca conduz pesquisa ou teste de usabilidade com usuários reais** — o agente não tem acesso a usuários reais nem telemetria de produto.
- Nunca gera PRD (Product Manager), Épicos/Stories (Product Owner) ou arquitetura técnica (Solution Architect).

## Arquitetura (resumo — detalhe completo em `docs/agent/system_design.md`)

- **`src/aqua_qe_ux_designer/models/`** — `UXSpecification`, `UserFlow`, `InformationArchitecture`, enum `ArtifactStatus`.
- **`src/aqua_qe_ux_designer/skills/`** — 17 funções de responsabilidade única (ver `docs/agent/skills.md`).
- **`src/aqua_qe_ux_designer/workflow/`** — orquestração da sequência de skills.
- **`src/aqua_qe_ux_designer/orchestrator/`** — ponto de entrada único (`handle_request`).
- **`src/aqua_qe_ux_designer/services/`** — `llm_service` (Ollama por padrão, mais um toggle de provedor em nuvem — `LLM_PROVIDER=nvidia|cerebras|google|groq`), `jira_service` (apenas leitura), `confluence_service` (leitura + escrita gated, reaproveitado do Solution Architect), `embedding_service`/`rag_service` (Ollama `bge-m3` + Qdrant embarcado — memória institucional de refinamento).

## Configuração

1. Instale [Python 3.12+](https://www.python.org/) e [uv](https://docs.astral.sh/uv/).
2. Instale o [Ollama](https://ollama.com) e baixe os três modelos locais usados por este agente:
   ```bash
   ollama pull mistral   # geração
   ollama pull phi4      # revisão independente
   ollama pull bge-m3    # embeddings (memória institucional de refinamento)
   ```
3. Instale as dependências:
   ```bash
   uv sync
   ```
4. Copie `.env.example` para `.env` e preencha os valores necessários (o Ollama funciona com os padrões; credenciais de Jira/Confluence são necessárias para `--jira`/`--confluence`/`--publicar-confluence`):
   ```bash
   cp .env.example .env
   ```

## Status detalhado

`docs/agent/` (PRD, System Design, Agent Design, Rules, Guardrails, Persona, Objectives, Skills, Evaluation, Memory) e `docs/standards/` estão completos. `knowledge/methodology/` tem os cinco documentos reais que fundamentam os critérios de qualidade (10 Heurísticas de Nielsen, WCAG 2.2, princípios de Arquitetura da Informação, ISO 9241-210, Laws of UX) — nenhum critério foi inventado à parte deles. `knowledge/templates/ux_specification.md` define o formato de exportação (12 seções, incluindo referências ao PRD e placeholders explícitos de fase futura).

`src/` (models/skills/workflow/orchestrator/services), `run.py` (CLI) e `tests/` (92 testes, 98% cobertura) estão implementados. Ver `WHITEPAPER.md`, seção 11, para o que segue deliberadamente fora desta fase.

---

**Eduardo Felizardo Cândido**
Senior QA Automation Engineer | AI-driven Testing | Robot Framework & Python
