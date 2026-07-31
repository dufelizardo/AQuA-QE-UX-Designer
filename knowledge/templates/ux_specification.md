# Template — UX Specification

> Estrutura padrão, sem conteúdo de domínio. Ver `../../docs/agent/output_schema.md` para o schema de dados exato.

## Campos

- **ID**: `<identificador único, ex.: UX-001>`
- **Título**: `<nome da tarefa/fluxo>`
- **Contexto e problema**: `<a tarefa/problema que motiva este fluxo, herdado da Story/Epic + PRD>`
- **Fluxos de Usuário**: `<lista de UserFlow — nome, passos em ordem, origem rastreável>`
- **Arquitetura da Informação**: `<seções/categorias de navegação e como se relacionam>`
- **Recomendações de Acessibilidade**: `<lista de recomendações fundamentadas em WCAG 2.1, sempre "a verificar", nunca certificação>`

## Relação com a hierarquia de artefatos

```
PRD (Product Manager)
 └── Épico / User Story (Product Owner)
      └── UX Specification (UX Designer)
           └── Wireframes / Protótipos (futuro UI Designer, fora de escopo nesta fase)
```

A UX Specification não substitui o PRD nem a Story — é a ponte entre "o que construir" (requisito funcional) e "como o usuário interage com isso" (fluxo de navegação), explicitando decisões de experiência que hoje ficam implícitas até a implementação. Não gera Personas nem User Journeys (já existem no PRD) e não gera Wireframes/Protótipos visuais (responsabilidade do futuro UI Designer).
