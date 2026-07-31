# Princípios de Arquitetura da Informação

> Fonte: princípios consolidados por Rosenfeld, Morville & Arango, "Information Architecture: For the Web and Beyond" (referência canônica da disciplina). Base para `design_information_architecture`.

## Princípios usados por este agente

1. **Princípio da categorização por tarefa do usuário** — agrupar conteúdo/funcionalidade pela tarefa que o usuário está tentando realizar, não pela estrutura interna do sistema ou do time que o construiu.
2. **Princípio de navegação previsível** — a localização de um item na estrutura de navegação deve ser consistente com onde um usuário esperaria encontrá-lo, dado o restante da estrutura.
3. **Princípio da profundidade razoável** (relacionado à Lei de Miller, "7±2") — preferir uma estrutura mais rasa e larga a uma estrutura muito profunda e estreita, quando a quantidade de conteúdo permitir escolha; profundidade excessiva aumenta a carga cognitiva para localizar um item.
4. **Princípio de nomenclatura consistente** — rótulos de seção/categoria usam a mesma convenção de linguagem em toda a estrutura (evitar misturar termos técnicos e termos do usuário para o mesmo conceito).

## Como este agente usa esses princípios

`design_information_architecture` gera `InformationArchitecture.sections` a partir do escopo do Épico, agrupado por tarefa do usuário (princípio 1), e `navigation_notes` explica como as seções se relacionam, verificando profundidade razoável (princípio 3) e nomenclatura consistente (princípio 4). Nenhuma seção é criada sem correspondência a um requisito real do Épico (GR-UX-1) — este documento orienta **como organizar** o que já existe na fonte, nunca **o que incluir** além dela.
