# Memory

> Estrutura conforme `../standards/memory_standard.md`. Decisão de produto nesta fase: **sem memória persistente** — cada execução é independente.

## Por que não há memória nesta fase

O agente processa uma Story/Epic por execução. Não há hoje um caso de uso real que exija lembrar decisões de fluxo entre execuções distintas — construir memória sem esse consumidor real seria especulativo (mesmo princípio de "não construir sem consumidor" já aplicado a `services/` em PM/PO/SA).

## Memória de sessão (curto prazo) — a única existente

- **O que**: as respostas do usuário durante o ciclo de refinamento (`--refinar`) da execução corrente.
- **Onde**: contexto da execução corrente, não persistido além dela.
- **Expiração**: descartada ao final da execução.

## Candidatos a memória futura (não implementados, não esquecidos)

- **Memória institucional de respostas de refinamento** (RAG) — mesma ideia já implementada nos agentes irmãos Product Manager e Product Owner: indexar respostas humanas dadas em ciclos de refinamento anteriores e sugerir uma resposta parecida quando uma pergunta semelhante aparecer de novo. Cotada como "oportunidade a considerar desde o dia 1" na spec deste agente (ver decisão registrada na memória de projeto da plataforma), mas não incluída na Fase 1 por padrão — decisão a confirmar quando a implementação real começar.
- **Memória de projeto**: se o agente passar a processar múltiplos Épicos relacionados do mesmo produto, lembrar decisões de fluxo já tomadas evitaria inconsistência de navegação entre features.

## Relação com o manifesto do agente

`agent_manifest.yaml` reflete esta decisão: `vector`/`rag`/`knowledge_graph` todos `false` nesta fase.
