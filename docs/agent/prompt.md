# Prompt

> Estrutura conforme `../standards/prompt_standard.md`. Este documento descreve a composição do prompt de sistema; o texto literal enviado ao LLM é implementação e deve apenas referenciar, não duplicar, o conteúdo dos documentos abaixo.

## Composição do prompt de sistema

1. **Papel/persona** — derivado integralmente de `persona.md` (consultivo, centrado no usuário, honesto sobre os limites do próprio papel).
2. **Objetivo da tarefa** — derivado de `objectives.md`, específico a cada skill (identificar fluxo, gerar arquitetura da informação, recomendar acessibilidade, etc. — ver `agent_design.md`).
3. **Instruções de comportamento** — derivadas de `ai_spec.md` (comportamento em caminho feliz, fonte ambígua e fora de escopo).
4. **Regras/guardrails reforçados** — RULE-UX-1 a RULE-UX-6 (`rules.md`) e os guardrails GR-UX-1 a GR-UX-4 (`guardrails.md`) devem aparecer de forma explícita e não negociável no prompt, não apenas implícita no tom. Em particular, `extract_ux_context` sempre instrui explicitamente para nunca gerar Persona/Journey nova (GR-UX-4).
5. **Formato de saída** — schema de `output_schema.md`, incluindo os valores válidos de `status`.
6. **Exemplos (few-shot)** — extraídos de `knowledge/examples/` quando existir (ainda não criado nesta fase); ausência de exemplos não deve degradar o comportamento esperado, apenas reduzir a calibração fina de estilo.

## Convenções de versionamento

- Cada versão do prompt é identificada, permitindo associar uma versão a um conjunto de resultados de `evaluation.md`.
- Mudanças que alterem comportamento observável (não apenas fraseado) exigem rodar os casos de teste de `evaluation.md` antes de substituir a versão em uso.

## O que o prompt não deve conter

- Não deve conter conhecimento de domínio específico de cliente diretamente embutido.
- Não deve reafirmar informações já garantidas estruturalmente pelo schema de saída.
- Não deve instruir o modelo a gerar Persona ou User Journey — isso violaria GR-UX-4 mesmo que a fonte pareça sugerir uma lacuna.
