# System Design

> Estrutura conforme `../standards/system_design_standard.md`.

## Visão geral da arquitetura

O agente é um pipeline de skills orquestrado sequencialmente, com dois pontos de checagem antes de qualquer saída ser considerada válida: validação automática (checklist estrutural) e revisão humana obrigatória — mesmo padrão de PM/PO/SA. Não há aprovação automática (ver `guardrails.md`).

```
Entrada (PRD via Confluence + Epics/Stories via Jira)
   → read_confluence_page (PRD) / read_jira_issue (Epic/Story)
   → extract_ux_context (título + contexto do problema; reaproveita Personas/Journeys já presentes no PRD)
   → identify_user_flows (por Story/tarefa)
   → design_information_architecture (por Épico)
   → review_accessibility (recomendações WCAG 2.2)
   → validate_ux_specification (checklist automático)
   → review_ux_specification (LLM revisor independente — phi4 — heurísticas de Nielsen)
   → [se reprovado] generate_ux_clarifying_questions → resposta humana → refine_ux_specification → revalidar
   → aceite humano explícito
   → format_ux_specification_markdown (export local)
   → [opcional] get_confluence_publish_location → create_confluence_page
```

## Componentes

- **Orquestrador** — ponto de entrada único (`handle_request`), decide a sequência de skills (ordem fixa do `agent_manifest.yaml`). Implementado em `../../src/aqua_qe_ux_designer/orchestrator/ux_designer.py`.
- **Workflow** — orquestração da sequência de skills (`generate_ux_specification`, `finalize_ux_specification`), implementado em `../../src/aqua_qe_ux_designer/workflow/`.
- **Skills** — funções descritas em `skills.md`, implementadas em `../../src/aqua_qe_ux_designer/skills/`.
- **Modelos de dados** — `UXSpecification`, `UserFlow`, `InformationArchitecture`, `ChatMessage`, enum `ArtifactStatus`, implementados em `../../src/aqua_qe_ux_designer/models/`, conforme `output_schema.md`.
- **Fontes de conhecimento** — `knowledge/methodology/` (10 Heurísticas de Nielsen, WCAG 2.2, princípios de Arquitetura da Informação, ISO 9241-210, Laws of UX), consumido diretamente no prompt de cada skill (sem RAG nesta fase — o volume cabe direto no contexto, mesma decisão de PM/SA na Fase 1).
- **Interfaces externas** — entrada: página Confluence (PRD, leitura) e ticket Jira (Epic/Story, leitura); saída: arquivo Markdown exportado (`format_ux_specification_markdown`) e, opcionalmente, uma página no Confluence (`create_confluence_page`), sempre irmã da página de origem do PRD e sempre atrás de confirmação humana.

## Fluxo de dados

1. A entrada é lida via `read_confluence_page` (PRD) e `read_jira_issue` (Epic/Story), sem escrita em nenhuma das duas nesta etapa.
2. `extract_ux_context` identifica título e contexto do problema; Personas/Journeys já presentes no texto do PRD são passadas como contexto às skills seguintes, nunca regeradas.
3. `identify_user_flows` gera o fluxo de navegação para a Story/tarefa em questão.
4. `design_information_architecture` gera o mapa de navegação do Épico.
5. `review_accessibility` gera recomendações WCAG 2.2 sobre o fluxo e a arquitetura da informação.
6. `validate_ux_specification` aplica o checklist automático; se reprovar, a UX Specification fica `pending_clarification`.
7. Se aprovado no checklist, `review_ux_specification` (LLM independente, fundamentado nas heurísticas de Nielsen) avalia o conjunto.
8. Se a revisão reprovar, o ciclo de refinamento humano-no-loop (mesmo padrão de PM/PO/SA) entra em ação.
9. A aprovação final é sempre um ato humano, fora da responsabilidade do agente — só então a UX Specification é exportada.

## Modos de operação

Um único fluxo nesta fase — gerar a UX Specification a partir de uma Story/Epic e do PRD associado. Sem distinção "unitário/lote" como em PM/PO — mesma razão de design do Solution Architect (só existe um artefato nesta fase).

## Restrições técnicas

- Dois LLMs locais via Ollama por padrão (`OLLAMA_MODEL` gerador, `OLLAMA_REVIEW_MODEL` revisor) — mesma convenção de PM/PO/SA.
- **Sem piloto de provedor em nuvem nesta fase** — diferente de PM/PO/SA (que adicionaram o toggle `LLM_PROVIDER` depois de necessidade real comprovada), este agente nasce só com Ollama; o toggle é adicionado quando/se surgir o mesmo tipo de necessidade (rate limit, instabilidade), não construído antecipadamente.
- Sem RAG/embeddings nesta fase — `knowledge/methodology/` é pequeno o suficiente para caber direto no prompt de cada skill.
- Jira é só leitura, sem escrita — mesmo princípio de "nenhum serviço construído sem consumidor real" já aplicado em PM/PO/SA (não há hoje um caso de uso real de write-back no Jira a partir de uma UX Specification). Confluence tem escrita gated (publicar), sempre atrás de confirmação humana e sempre como página irmã da fonte — reaproveita literalmente o `confluence_service.py` do Solution Architect (`get_confluence_publish_location`/`create_confluence_page`, já provado).

## Observabilidade

- Cada execução deve registrar: fonte de entrada (PRD + Story/Epic), fluxos de usuário e arquitetura da informação identificados, resultado do checklist automático e da revisão, e se houve ciclo de refinamento — necessário para auditar rastreabilidade (ver `guardrails.md`) e para os casos de teste de `evaluation.md`.
