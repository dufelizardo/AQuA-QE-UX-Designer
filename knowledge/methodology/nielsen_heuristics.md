# As 10 Heurísticas de Usabilidade de Nielsen

> Fonte: Jakob Nielsen, Nielsen Norman Group ("10 Usability Heuristics for User Interface Design", 1994, revisado 2020). Base para `review_ux_specification` — o agente avalia `UserFlow`/`InformationArchitecture` contra estas heurísticas, sempre como avaliação heurística de especialista, nunca como teste com usuário real (GR-UX-3).

1. **Visibilidade do status do sistema** — o sistema deve sempre manter o usuário informado sobre o que está acontecendo, com feedback apropriado em tempo razoável.
2. **Correspondência entre o sistema e o mundo real** — o sistema deve falar a língua do usuário, com palavras/frases/conceitos familiares, seguindo convenções do mundo real.
3. **Controle e liberdade do usuário** — usuários frequentemente escolhem funções por engano e precisam de uma "saída de emergência" claramente marcada para sair do estado indesejado sem precisar de um diálogo extenso.
4. **Consistência e padrões** — usuários não devem ter que se perguntar se palavras, situações ou ações diferentes significam a mesma coisa; seguir convenções da plataforma.
5. **Prevenção de erros** — melhor que boas mensagens de erro é um design cuidadoso que previne o problema desde o início.
6. **Reconhecimento em vez de memorização** — minimizar a carga de memória do usuário, tornando objetos, ações e opções visíveis; instruções de uso devem ser visíveis ou facilmente recuperáveis.
7. **Flexibilidade e eficiência de uso** — aceleradores, invisíveis para o usuário novato, podem acelerar a interação para o usuário experiente.
8. **Estética e design minimalista** — diálogos não devem conter informação irrelevante ou raramente necessária; toda unidade extra de informação compete com as unidades relevantes.
9. **Ajudar os usuários a reconhecer, diagnosticar e se recuperar de erros** — mensagens de erro em linguagem simples (sem código), indicando precisamente o problema e sugerindo uma solução construtiva.
10. **Ajuda e documentação** — mesmo que seja melhor que o sistema possa ser usado sem documentação, pode ser necessário fornecer ajuda/documentação, fácil de buscar, focada na tarefa do usuário.

## Como este agente usa essas heurísticas

`review_ux_specification` avalia cada `UserFlow` gerado contra as heurísticas relevantes (tipicamente 1, 3, 4, 5, 6, 9 para fluxos de navegação) e cada `InformationArchitecture` contra as heurísticas de organização/consistência (2, 4, 8). Os apontamentos ficam em `review_notes`, sempre referenciando a heurística específica violada — nunca uma crítica genérica de "não é intuitivo".
