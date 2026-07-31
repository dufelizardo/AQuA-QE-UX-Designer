# Skills

> **Nota de fase**: este documento descreve as skills da Fase 1, na ordem do `agent_manifest.yaml` — todas implementadas em `../../src/aqua_qe_ux_designer/skills/`, no formato definido em `../standards/skill_standard.md`. Tipos de entrada/saída referem-se às estruturas de `output_schema.md`, implementadas em `../../src/aqua_qe_ux_designer/models/`.
>
> `extract_ux_context`, `identify_user_flows`, `design_information_architecture`, `review_accessibility`, `generate_ux_clarifying_questions` e `refine_ux_specification` usarão o LLM gerador (`../../src/aqua_qe_ux_designer/services/llm_service.py::generator_model()`; Ollama local, `OLLAMA_MODEL`/padrão `mistral` — sem piloto de provedor em nuvem nesta fase, ver `system_design.md`). `validate_ux_specification` e `format_ux_specification_markdown` serão Python puro, sem LLM (ver `evaluation.md`). `review_ux_specification` usará o LLM revisor (`llm_service.py::reviewer_model()`; Ollama `OLLAMA_REVIEW_MODEL`/padrão `phi4`), sempre diferente do gerador, fundamentado nas 10 Heurísticas de Nielsen. `read_jira_issue`/`read_confluence_page` usarão a API REST do Jira/Confluence Cloud — **apenas leitura**. `create_confluence_page`/`get_confluence_publish_location` **escreverão** no Confluence Cloud (Jira continua apenas leitura) — sempre atrás de confirmação humana explícita no CLI (`run.py`), reaproveitando o padrão já provado no Solution Architect.

## read_confluence_page

- **Descrição**: busca uma página do Confluence Cloud (o PRD de origem, aceita URL completa ou ID) e retorna título + corpo como texto simples, convertendo do storage format (XHTML). Apenas leitura.
- **Entrada**: `pagina: str` (URL completa ou ID).
- **Saída**: `str`.
- **Efeitos colaterais**: chamada HTTP `GET` ao Confluence Cloud.
- **Erros esperados**: credencial ausente, página inexistente ou sem permissão (HTTP 4xx).
- **Dependências**: nenhuma outra skill. Reaproveita `confluence_service.py`, portado do Solution Architect.

## read_jira_issue

- **Descrição**: busca um ticket Jira (Epic ou Story) e retorna como texto simples, convertendo do Atlassian Document Format. Apenas leitura — este agente nunca escreve de volta no Jira.
- **Entrada**: `issue_key: str` (ex.: `"AQUAQE-10"`).
- **Saída**: `str`.
- **Efeitos colaterais**: chamada HTTP `GET` ao Jira Cloud.
- **Erros esperados**: credencial ausente, ticket inexistente ou sem permissão.
- **Dependências**: nenhuma outra skill.

## get_confluence_publish_location

- **Descrição**: deriva o espaço/ancestral de publicação a partir da página de origem do PRD, para que a UX Specification seja publicada como página irmã — nunca de configuração manual solta (RULE-UX-6). Reaproveita o mesmo padrão já provado no Solution Architect.
- **Entrada**: `pagina_origem: str` (URL/ID do PRD).
- **Saída**: `dict` (espaço + ID do ancestral).
- **Efeitos colaterais**: chamada HTTP `GET` ao Confluence Cloud.
- **Erros esperados**: página de origem sem página-mãe identificável.
- **Dependências**: consome a mesma fonte de `read_confluence_page`.

## create_confluence_page

- **Descrição**: cria a UX Specification como página nova no Confluence Cloud, sempre como irmã da página de origem do PRD. Só é chamada pelo CLI após confirmação humana explícita (RULE-UX-6).
- **Entrada**: `titulo: str`, `corpo: str` (Markdown convertido para storage format), `espaco: str`, `ancestral_id: str`.
- **Saída**: `str` (URL/ID da página criada).
- **Efeitos colaterais**: chamada HTTP `POST` ao Confluence Cloud — **escreve** em sistema externo.
- **Erros esperados**: credencial ausente, espaço/ancestral inválido.
- **Dependências**: consome `get_confluence_publish_location` e `format_ux_specification_markdown`.

## extract_ux_context

- **Descrição**: extrai título e contexto do problema/tarefa a partir do PRD + Story/Epic combinados. Reaproveita as seções de Personas e de User Journey já presentes no texto do PRD como contexto de leitura, **separadamente** — **nunca gera uma Persona ou Journey nova** (GR-UX-4). Se o PRD não tiver uma das duas seções (ou nenhuma), o campo correspondente volta vazio — isso é sinalizado como lacuna do PRD por `validate_ux_specification`, nunca preenchido por suposição.
- **Entrada**: `texto_prd: str`, `texto_story_ou_epic: str`.
- **Saída**: `dict` (`title`, `context_problem`, `personas_reference`, `journey_reference` — os dois últimos vazios se ausentes no PRD).
- **Efeitos colaterais**: chamada ao LLM gerador.
- **Erros esperados**: resposta do LLM não é JSON válido.
- **Dependências**: consome a saída de `read_confluence_page`/`read_jira_issue`.

## identify_user_flows

- **Descrição**: identifica o fluxo de navegação concreto (sequência de passos/telas) para completar a tarefa descrita na Story, rastreável ao requisito de origem. Mais granular que a User Journey do PM — nível de navegação, não de jornada de negócio (ver `agent_design.md`, item 3). Organiza os passos considerando a Lei de Hick e a Lei de Jakob (`../../knowledge/methodology/laws_of_ux.md`) — nunca como justificativa para adicionar um passo sem base real na Story (GR-UX-1).
- **Entrada**: `texto_story: str`, `contexto: dict` (de `extract_ux_context`).
- **Saída**: `UserFlow` (`name`, `steps: list[str]`, `source_reference`).
- **Efeitos colaterais**: chamada ao LLM gerador.
- **Erros esperados**: resposta do LLM não é JSON válido; Story sem informação suficiente para inferir um fluxo (retorna fluxo vazio/curto, nunca inventa passos — GR-UX-1).
- **Dependências**: consome a saída de `extract_ux_context`.

## design_information_architecture

- **Descrição**: gera o mapa de navegação/categorização para o escopo do Épico, seguindo os princípios de `../../knowledge/methodology/information_architecture.md` (categorização por tarefa, profundidade razoável) e a Lei de Miller/Carga Cognitiva (`../../knowledge/methodology/laws_of_ux.md`).
- **Entrada**: `texto_epic: str`, `contexto: dict`.
- **Saída**: `InformationArchitecture` (`sections: list[str]`, `navigation_notes: str`, `source_reference`).
- **Efeitos colaterais**: chamada ao LLM gerador.
- **Erros esperados**: resposta do LLM não é JSON válido.
- **Dependências**: consome a saída de `extract_ux_context`.

## review_accessibility

- **Descrição**: gera recomendações de acessibilidade fundamentadas em WCAG 2.2 (`../../knowledge/methodology/wcag.md`) sobre o `UserFlow`/`InformationArchitecture` — sempre como recomendação a verificar, nunca certificação de conformidade (GR-UX-2).
- **Entrada**: `user_flow: UserFlow`, `information_architecture: InformationArchitecture`.
- **Saída**: `list[str]`.
- **Efeitos colaterais**: chamada ao LLM gerador.
- **Erros esperados**: resposta do LLM não é JSON válido.
- **Dependências**: consome a saída de `identify_user_flows`/`design_information_architecture`.

## validate_ux_specification

- **Descrição**: valida a UX Specification contra o checklist automático (`validation_checklist.md`) e retorna os motivos específicos de reprovação — mesmo contrato `list[str]` já corrigido nos agentes irmãos (nunca `bool` sem motivo). Inclui checar `personas_reference`/`journey_reference` (separadamente): se o PRD de origem não tinha uma dessas seções, a UX Specification reprova até o ciclo de esclarecimento humano-no-loop suprir a lacuna.
- **Entrada**: `spec: UXSpecification`.
- **Saída**: `list[str]` — motivos de reprovação, acumulando todos; lista vazia = aprovado no checklist.
- **Efeitos colaterais**: nenhum — Python puro, sem LLM.
- **Erros esperados**: nenhum.
- **Dependências**: consome a saída de `identify_user_flows`/`design_information_architecture`/`review_accessibility`.

## review_ux_specification

- **Descrição**: revisa a UX Specification com um LLM diferente do gerador, fundamentado nas 10 Heurísticas de Nielsen (`../../knowledge/methodology/nielsen_heuristics.md`) e nas Laws of UX (`../../knowledge/methodology/laws_of_ux.md`) — sempre rotulado como avaliação heurística de especialista, nunca como teste com usuário real (GR-UX-3).
- **Entrada**: `spec: UXSpecification`.
- **Saída**: `dict` (`aprovado: bool`, `problemas: list[str]`).
- **Efeitos colaterais**: chamada ao LLM revisor.
- **Erros esperados**: resposta do LLM não é JSON válido.
- **Dependências**: roda depois de `validate_ux_specification` aprovar.

## generate_ux_clarifying_questions

- **Descrição**: transforma os apontamentos de `review_notes` em perguntas objetivas para o usuário.
- **Entrada**: `spec: UXSpecification`.
- **Saída**: `list[str]`.
- **Efeitos colaterais**: chamada ao LLM gerador.
- **Erros esperados**: resposta do LLM não é JSON válido.
- **Dependências**: consome `review_notes`, preenchido por `validate_ux_specification` ou `review_ux_specification`.

## refine_ux_specification

- **Descrição**: reescreve os campos afetados pelas respostas do usuário, preservando o texto existente nos campos que as respostas não abordam — mesmo cuidado já aplicado em `refine_solution_design`/`refine_epic_metadata` nos agentes irmãos, aprendido com um bug real de obsolescência.
- **Entrada**: `spec: UXSpecification`, `respostas: list[dict]` (`{"pergunta": str, "resposta": str}`).
- **Saída**: `UXSpecification`.
- **Efeitos colaterais**: chamada ao LLM gerador.
- **Erros esperados**: resposta do LLM não é JSON válido.
- **Dependências**: consome `generate_ux_clarifying_questions` + resposta humana coletada pelo CLI.

## format_ux_specification_markdown

- **Descrição**: exporta a UX Specification em Markdown, seguindo as 12 seções de `../../knowledge/templates/ux_specification.md`. Preenche as seções geradas por este agente (Objetivo, User Flows, Information Architecture, Acessibilidade, Regras de Usabilidade, Recomendações); Escopo cita `prd_reference`/`ticket_reference` (link/chave, não o texto completo); Personas/User Journey citam `personas_reference`/`journey_reference` extraídos do PRD (ou o aviso de ausência); Wireframes/Protótipos/Design System ficam marcados como fora de escopo desta fase — nunca preenchidos com conteúdo gerado por este agente (GR-UX-4). A seção "Rastreabilidade" final é uma tabela de/para (artefato → trecho de origem), não um dump do texto completo da fonte.
- **Entrada**: `spec: UXSpecification`.
- **Saída**: `str`.
- **Efeitos colaterais**: nenhum — Python puro, sem LLM.
- **Erros esperados**: nenhum.
- **Dependências**: consome a saída final de `refine_ux_specification` (ou a saída inicial, se aprovada sem refino).
