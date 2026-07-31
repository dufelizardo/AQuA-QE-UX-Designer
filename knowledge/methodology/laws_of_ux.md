# Laws of UX

> Fonte: Jon Yablonski, "Laws of UX" (lawsofux.com) — compilação de princípios cognitivos e heurísticos aplicados ao design de interação, cada um com base em pesquisa de psicologia cognitiva real e citável. Diferente das Heurísticas de Nielsen (avaliação qualitativa ampla), estas leis são regras concretas e diretamente operacionalizáveis em decisões específicas de fluxo/arquitetura da informação.

## Leis usadas por este agente

1. **Lei de Hick** (Hick's Law) — o tempo para tomar uma decisão aumenta com o número e complexidade das opções. Usada por `identify_user_flows`: preferir menos opções por passo do fluxo, quando o requisito de origem permitir essa simplificação sem perder informação.
2. **Lei de Fitts** (Fitts's Law) — o tempo para atingir um alvo depende da distância até ele e do seu tamanho. Menos aplicável diretamente (é uma lei de design visual/motor, mais relevante ao futuro UI Designer), mas informa recomendações de acessibilidade sobre tamanho de alvo de toque (ver WCAG 2.2, critério 2.5.8).
3. **Lei de Jakob** (Jakob's Law) — usuários passam a maior parte do tempo em *outros* produtos; eles preferem que o seu produto funcione da mesma forma que os produtos que já conhecem. Usada por `identify_user_flows`/`design_information_architecture`: preferir padrões de navegação convencionais a soluções não convencionais, quando a fonte não exigir explicitamente algo diferente.
4. **Lei de Miller** (Miller's Law, "7±2") — a memória de trabalho tem capacidade limitada. Já usada em `knowledge/methodology/information_architecture.md` (princípio da profundidade razoável) — citada aqui formalmente como a base real desse princípio.
5. **Carga Cognitiva** (Cognitive Load) — princípio geral de que a interface deve minimizar o esforço mental necessário para completar uma tarefa. Usada por `design_information_architecture`: agrupar/categorizar por tarefa do usuário (não por estrutura interna do sistema) para reduzir carga cognitiva de navegação.

## Como este agente usa estas leis

`identify_user_flows` e `design_information_architecture` usam estas leis como critério de **como organizar** o que já existe na fonte (GR-UX-1 continua valendo — nenhuma lei justifica adicionar um passo/seção sem base real na Story/Epic). `review_ux_specification` também pode citar uma lei específica ao apontar um problema (ex.: "este fluxo viola a Lei de Hick — 6 opções apresentadas simultaneamente sem agrupamento"), da mesma forma que cita as Heurísticas de Nielsen.
