# PRD — AQuA-QE UX Designer

> Estrutura conforme `../standards/prd_standard.md`.

## Contexto e problema

Requisitos funcionais (PRD do Product Manager, Épicos/Stories do Product Owner) descrevem **o que** o sistema deve fazer, mas raramente descrevem **como** o usuário navega para completar cada tarefa. Sem essa camada, decisões de fluxo de navegação e organização de conteúdo ficam implícitas — ou terceirizadas informalmente para quem implementa, gerando interfaces inconsistentes entre features do mesmo produto e retrabalho quando a experiência real não atende à expectativa do usuário.

## Objetivo do produto

Gerar uma UX Specification a partir de um PRD (Product Manager) e das Épicos/Stories já detalhadas (Product Owner), cobrindo fluxos de navegação concretos por tarefa, arquitetura da informação e recomendações de acessibilidade — com rastreabilidade total à fonte e revisão humana obrigatória antes de qualquer aceite. **Nunca regera Personas ou User Journeys** — esses artefatos já existem no PRD do Product Manager (`synthesize_personas`/`identify_user_journeys`) e são consumidos como contexto, nunca re-derivados.

## Público-alvo / personas

- **UX/Product Designer** — usa a UX Specification gerada como ponto de partida para wireframes/protótipos (hoje fora do escopo deste agente — ver `WHITEPAPER.md`).
- **Product Owner** — consulta os fluxos para refinar critérios de aceitação de uma Story em termos de interação.
- **Solution Architect** — consome a UX Specification junto com o PRD/backlog ao desenhar a arquitetura técnica, garantindo que a solução suporte os fluxos definidos.

## Escopo (Fase 1)

- Ler o PRD via Confluence (leitura) — mesma fonte que Product Owner/Solution Architect já leem, incluindo as seções de Personas/Journeys já existentes, consumidas como contexto.
- Ler Épicos/Stories via Jira (leitura apenas).
- Para cada Story/Epic, identificar um Fluxo de Usuário (`UserFlow`) — sequência concreta de passos/telas de navegação para completar a tarefa descrita.
- Gerar uma Arquitetura da Informação (`InformationArchitecture`) — mapa de navegação/categorização do escopo do Épico.
- Gerar recomendações de acessibilidade fundamentadas em WCAG 2.2, sempre como recomendação a verificar, nunca afirmação de conformidade.
- Avaliar os fluxos por meio de revisão heurística (10 Heurísticas de Nielsen) — nunca chamada de "teste de usabilidade" (não há usuário real envolvido).
- Validar a saída contra um checklist automático antes de apresentá-la.
- Suportar ciclo de refinamento humano-no-loop (perguntas de esclarecimento → resposta humana → refino).
- Exportar o resultado em Markdown.
- Publicar o resultado como página no Confluence Cloud, sempre como irmã da página de origem do PRD e sempre atrás de confirmação humana explícita.

## Fora de escopo (Fase 1 — ver WHITEPAPER seção 11 para detalhe)

- **Personas e User Journeys** — permanentemente fora: já são responsabilidade do agente irmão AQuA-QE Product Manager; gerá-los aqui também criaria duas fontes divergentes do mesmo artefato.
- **Wireframes, Protótipos e Design System** — via Figma real (leitura/escrita) — responsabilidade do futuro agente irmão AQuA-QE UI Designer, ainda não iniciado. Esta é a primeira integração não-textual da plataforma; deliberadamente adiada até esse agente existir.
- **Pesquisa com usuário real** (entrevistas, observação, pesquisas) e **Testes de Usabilidade reais** (com usuários observados) — permanentemente fora: o agente não tem acesso a usuários reais nem telemetria de produto; qualquer versão honesta dessas especialidades exigiria uma fonte de dado que não existe. Substituídas por revisão heurística de especialista (Nielsen), nunca apresentada como pesquisa/teste real.
- Integrações com Maze, Hotjar, Google Analytics, Mixpanel, Amplitude — mesma razão acima.
- Escrita em Jira (o agente só lê essa fonte, mesmo princípio do Solution Architect).
- Piloto de provedor de LLM em nuvem (`LLM_PROVIDER=ollama|nvidia|cerebras|google|groq`, padrão `ollama`) — implementado após necessidade real comprovada (rodadas locais lentas em uso real), mesmo padrão adotado nos três agentes irmãos.
- RAG/memória de projeto ou longo prazo.

## Requisitos funcionais

1. Ler e interpretar o PRD via Confluence e Épicos/Stories via Jira.
2. Extrair título e contexto do problema a partir da fonte (reaproveitando Personas/Journeys já presentes no PRD como contexto, nunca regerando).
3. Identificar um Fluxo de Usuário concreto por Story/tarefa, rastreável ao requisito de origem.
4. Gerar uma Arquitetura da Informação para o escopo do Épico.
5. Gerar recomendações de acessibilidade fundamentadas em WCAG 2.2.
6. Avaliar os fluxos via revisão heurística fundamentada nas 10 Heurísticas de Nielsen.
7. Validar a saída contra um checklist automático (ao menos 1 fluxo + IA presente) antes de apresentá-la.
8. Revisar com um segundo LLM independente do gerador.
9. Quando a revisão reprovar, gerar perguntas de esclarecimento e refinar com as respostas humanas.
10. Exportar o resultado validado em Markdown.
11. Publicar no Confluence como página irmã do PRD, sempre atrás de confirmação humana.

## Requisitos não funcionais

- **Rastreabilidade** — todo passo de fluxo gerado deve ser rastreável a um requisito real da Story/Epic de origem.
- **Nenhuma aprovação automática** — toda saída é um rascunho validado, sujeito a revisão humana obrigatória.
- **Nunca afirmar certeza não verificada** — recomendações de acessibilidade e achados de revisão heurística são sempre rotulados como recomendação/avaliação de especialista, nunca como fato comprovado com usuários reais.
- **Consistência de formato** — toda saída segue o template em `../../knowledge/templates/ux_specification.md`.

## Métricas de sucesso

- Taxa de aceitação sem retrabalho — % de UX Specifications geradas aceitas sem edição substancial.
- Cobertura de rastreabilidade — % de passos de fluxo com `source_reference` preenchido a partir da fonte real.
- Redução de inconsistência de navegação entre features do mesmo produto (medida qualitativamente, via revisão humana).

## Riscos e premissas

- Premissa: a Story/Epic de origem contém informação suficiente para inferir um fluxo de navegação plausível na maioria dos casos; quando não contém, o agente deve refletir isso via `pending_clarification`, nunca inventar passos.
- Risco: Stories muito abstratas ou sem critérios de aceitação detalhados podem limitar a qualidade do fluxo gerado.
- Risco: sem Wireframes/Protótipos reais (Fase 2, UI Designer), a UX Specification desta fase é só textual — útil para alinhamento, mas não substitui uma validação visual real antes da implementação.
