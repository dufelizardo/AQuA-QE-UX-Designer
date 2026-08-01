# Memory

> Estrutura conforme `../standards/memory_standard.md`.

## Memória de sessão (curto prazo)

- **O que**: as respostas do usuário durante o ciclo de refinamento (`--refinar`) da execução corrente.
- **Onde**: contexto da execução corrente, não persistido além dela.
- **Expiração**: descartada ao final da execução.

## Memória institucional de respostas de refinamento (RAG) — implementada

Mesma ideia já validada ao vivo nos agentes irmãos Product Manager ([#9](https://github.com/dufelizardo/AQuA-QE-Product-Manager/issues/9)) e Product Owner ([#12](https://github.com/dufelizardo/AQuA-QE-Product-Owner/issues/12)), portada para este agente ([#3](https://github.com/dufelizardo/AQuA-QE-UX-Designer/issues/3)):

- Cada resposta não vazia que o humano dá a uma pergunta de esclarecimento do ciclo de refinamento é gravada (`record_refinement_answer`) numa collection Qdrant embarcada própria (`refinement_answer_memory`), via embedding local (Ollama `bge-m3`).
- No ciclo seguinte (mesmo ou de outro artefato/projeto), se uma pergunta parecida aparecer, `suggest_refinement_answer` exibe a resposta mais similar já dada, com o score de similaridade — **nunca aplicada automaticamente**: o humano sempre digita a resposta no `input()` normalmente.
- Sem gate de score mínimo (sem corpus histórico para calibrar um threshold) e sem filtro por `tipo_artefato` (aqui sempre `"ux_specification"`, já que este agente só tem um artefato — mas a collection é compartilhada com outros projetos/execuções, o valor da ideia é a reciprocidade).
- Esta é a primeira infraestrutura de embedding/vetor deste agente — construída especificamente para este consumidor real, não antecipadamente (mesmo princípio já aplicado nos agentes irmãos).

## Memória de projeto (ainda não implementada)

Se o agente passar a processar múltiplos Épicos relacionados do mesmo produto, lembrar decisões de fluxo já tomadas evitaria inconsistência de navegação entre features — não há hoje um consumidor real para isso.

## Relação com o manifesto do agente

`agent_manifest.yaml` reflete esta decisão: `vector`/`rag` agora `true` (memória de refinamento); `knowledge_graph` continua `false`.
