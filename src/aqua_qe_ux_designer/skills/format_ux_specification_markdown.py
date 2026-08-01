from ..models import UXSpecification


def _lista_md(itens: list[str]) -> str:
    return "\n".join(f"- {item}" for item in itens) if itens else "(nenhum)"


def _fluxos_md(spec: UXSpecification) -> str:
    if not spec.user_flows:
        return "(nenhum)"
    linhas = []
    for fluxo in spec.user_flows:
        linhas.append(f"### {fluxo.name}")
        linhas.append("")
        linhas += [f"{i + 1}. {passo}" for i, passo in enumerate(fluxo.steps)]
        linhas.append("")
    return "\n".join(linhas).rstrip()


def _referencia_prd_md(referencia: str, rotulo: str) -> str:
    if referencia:
        return referencia
    return f"> Não disponível no PRD de origem — nenhuma {rotulo} identificada."


_TOPICO_MAX_CARACTERES = 80
_TOPICO_MAX_PALAVRAS = 10


def _regra_usabilidade_md(nota: str) -> str:
    """Destaca o tópico da observação heurística, quando houver um separador reconhecível
    (' — ' ou ': ') e o trecho antes dele for curto o suficiente para ser um tópico, não uma
    frase comum que só contém dois-pontos no meio."""
    if " — " in nota:
        topico, resto = nota.split(" — ", 1)
        return f"- **{topico}** — {resto}"
    if ": " in nota:
        topico, resto = nota.split(": ", 1)
        if len(topico) <= _TOPICO_MAX_CARACTERES and len(topico.split()) <= _TOPICO_MAX_PALAVRAS:
            return f"- **{topico}**: {resto}"
    return f"- {nota}"


def _regras_usabilidade_md(notas: list[str]) -> str:
    return "\n".join(_regra_usabilidade_md(nota) for nota in notas) if notas else "(nenhuma)"


_TRECHO_MAX_CARACTERES = 200


def _trecho_para_tabela(trecho: str) -> str:
    """Achata um trecho de origem para uma única linha e limita o tamanho, para nunca quebrar
    a sintaxe de tabela Markdown (uma linha de tabela precisa ficar numa única linha) nem
    inflar a tabela com o texto completo da fonte — achado ao vivo: identify_user_flows às
    vezes devolve o PRD inteiro como trecho_fonte em vez de um excerto curto."""
    texto = " ".join(trecho.split())
    if len(texto) > _TRECHO_MAX_CARACTERES:
        texto = texto[:_TRECHO_MAX_CARACTERES].rstrip() + "…"
    return texto or "(não informado)"


def _rastreabilidade_md(spec: UXSpecification) -> str:
    """Tabela de/para: cada artefato gerado, ligado ao trecho da fonte que o originou (GR-UX-1)."""
    linhas = [
        "| Artefato | Trecho de origem |",
        "|---|---|",
        f"| PRD de origem | {spec.prd_reference or '(não informado)'} |",
        f"| Story/Epic de origem | {spec.ticket_reference or '(não informado)'} |",
    ]
    for fluxo in spec.user_flows:
        linhas.append(f"| User Flow: {fluxo.name} | {_trecho_para_tabela(fluxo.source_reference)} |")
    if spec.information_architecture.sections:
        linhas.append(
            f"| Information Architecture | {_trecho_para_tabela(spec.information_architecture.source_reference)} |"
        )
    return "\n".join(linhas)


def format_ux_specification_markdown(spec: UXSpecification) -> str:
    """Formata a UX Specification em Markdown, seguindo as 12 seções de knowledge/templates/ux_specification.md."""
    ia = spec.information_architecture
    return (
        f"# {spec.title or spec.id}\n\n"
        f"**ID**: {spec.id}\n"
        f"**Status**: {spec.status.value}\n\n"
        f"## 1. Objetivo\n{spec.context_problem}\n\n"
        "## 2. Escopo\n"
        f"- **PRD de origem**: {spec.prd_reference or '(não informado)'}\n"
        f"- **Story/Epic de origem**: {spec.ticket_reference or '(não informado)'}\n\n"
        "## 3. Personas\n\n"
        "> Não gerado por este agente — as Personas relevantes a esta tarefa devem ser "
        "extraídas literalmente do PRD de origem (Product Manager) e citadas abaixo, nunca "
        "criadas por este agente (GR-UX-4).\n\n"
        f"{_referencia_prd_md(spec.personas_reference, 'seção de Personas')}\n\n"
        f"## 4. User Flows\n\n{_fluxos_md(spec)}\n\n"
        "## 5. Information Architecture\n\n"
        f"Seções:\n\n{_lista_md(ia.sections)}\n\n"
        f"Notas de navegação: {ia.navigation_notes or '(nenhuma)'}\n\n"
        f"## 6. Recomendações de Acessibilidade\n{_lista_md(spec.accessibility_recommendations)}\n\n"
        "## 7. User Journey\n\n"
        "> Não gerado por este agente — a User Journey relevante a esta tarefa deve ser "
        "extraída literalmente do PRD de origem (Product Manager, seção 'Jornadas do "
        "Usuário') e citada abaixo, nunca criada por este agente (GR-UX-4). Nível de "
        "negócio/emocional, diferente dos User Flows de navegação concreta da seção 4.\n\n"
        f"{_referencia_prd_md(spec.journey_reference, 'seção de User Journey')}\n\n"
        "## 8. Wireframes\n\n"
        "> Fora de escopo desta fase — gerar wireframes exige integração com uma ferramenta "
        "de design visual (Figma), que a plataforma ainda não tem. Esta seção existe para "
        "manter a estrutura completa do documento; quando o futuro agente irmão AQuA-QE UI "
        "Designer for implementado, ele preencherá aqui o(s) link(s) para o(s) wireframe(s) "
        "correspondente(s) aos User Flows da seção 4.\n\n"
        "## 9. Protótipos\n\n"
        "> Fora de escopo desta fase, mesma razão da seção 8 — protótipos interativos "
        "dependem dos wireframes existirem primeiro. Preenchida pelo futuro AQuA-QE UI "
        "Designer.\n\n"
        "## 10. Regras de Usabilidade\n\n"
        "> Avaliação heurística de especialista (10 Heurísticas de Nielsen + Laws of UX) — "
        "nunca um teste com usuário real (GR-UX-3).\n\n"
        f"{_regras_usabilidade_md(spec.review_notes)}\n\n"
        "## 11. Design System\n\n"
        "> Fora de escopo desta fase, mesma razão da seção 8 — contribuições de Design "
        "System (novos componentes/variações) dependem de Wireframes/Protótipos existirem "
        "primeiro. Preenchida pelo futuro AQuA-QE UI Designer.\n\n"
        "## 12. Recomendações\n\n"
        "> Síntese priorizada das recomendações de acessibilidade (seção 6) e observações de "
        "usabilidade (seção 10) acima — nunca inclui um item que não esteja em uma das duas "
        "seções.\n\n"
        f"{_lista_md(spec.recommendations_synthesis)}\n\n"
        f"## Rastreabilidade\n\n{_rastreabilidade_md(spec)}\n"
    )
