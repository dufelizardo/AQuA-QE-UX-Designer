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


def _regra_usabilidade_md(nota: str) -> str:
    """Destaca o tópico da observação heurística (antes do primeiro ' — '), quando houver."""
    if " — " in nota:
        topico, resto = nota.split(" — ", 1)
        return f"- **{topico}** — {resto}"
    return f"- {nota}"


def _regras_usabilidade_md(notas: list[str]) -> str:
    return "\n".join(_regra_usabilidade_md(nota) for nota in notas) if notas else "(nenhuma)"


def _rastreabilidade_md(spec: UXSpecification) -> str:
    """Tabela de/para: cada artefato gerado, ligado ao trecho da fonte que o originou (GR-UX-1)."""
    linhas = [
        "| Artefato | Trecho de origem |",
        "|---|---|",
        f"| PRD de origem | {spec.prd_reference or '(não informado)'} |",
        f"| Story/Epic de origem | {spec.ticket_reference or '(não informado)'} |",
    ]
    for fluxo in spec.user_flows:
        linhas.append(f"| User Flow: {fluxo.name} | {fluxo.source_reference or '(não informado)'} |")
    if spec.information_architecture.sections:
        origem_ia = spec.information_architecture.source_reference or "(não informado)"
        linhas.append(f"| Information Architecture | {origem_ia} |")
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
        "> Não gerado por este agente — apenas referência às Personas já existentes no PRD "
        "de origem (Product Manager).\n\n"
        f"{_referencia_prd_md(spec.personas_reference, 'seção de Personas')}\n\n"
        f"## 4. User Flows\n\n{_fluxos_md(spec)}\n\n"
        "## 5. Information Architecture\n\n"
        f"Seções: {_lista_md(ia.sections)}\n\n"
        f"Notas de navegação: {ia.navigation_notes or '(nenhuma)'}\n\n"
        f"## 6. Recomendações de Acessibilidade\n{_lista_md(spec.accessibility_recommendations)}\n\n"
        "## 7. User Journey\n\n"
        "> Não gerado por este agente — apenas referência à User Journey já existente no PRD "
        "de origem (Product Manager). Nível de negócio/emocional, diferente dos User Flows "
        "de navegação concreta da seção 4.\n\n"
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
        f"Antes da implementação, revisar as recomendações de acessibilidade (seção 6, "
        f"{len(spec.accessibility_recommendations)} item(ns)) e as observações de "
        f"usabilidade (seção 10, {len(spec.review_notes)} item(ns)) acima.\n\n"
        f"## Rastreabilidade\n\n{_rastreabilidade_md(spec)}\n"
    )
