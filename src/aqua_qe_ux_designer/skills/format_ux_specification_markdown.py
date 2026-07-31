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


def format_ux_specification_markdown(spec: UXSpecification) -> str:
    """Formata a UX Specification em Markdown, seguindo as 12 seções de knowledge/templates/ux_specification.md."""
    ia = spec.information_architecture
    return (
        f"# {spec.title or spec.id}\n\n"
        f"**ID**: {spec.id}\n"
        f"**Status**: {spec.status.value}\n\n"
        f"## 1. Objetivo\n{spec.context_problem}\n\n"
        f"## 2. Escopo\n{spec.source_reference}\n\n"
        "## 3. Personas\n\n"
        "> Não gerado por este agente. Referência às Personas já existentes no PRD de "
        "origem (Product Manager) — não disponível no PRD de origem, se não citado como "
        "contexto.\n\n"
        f"## 4. User Flows\n\n{_fluxos_md(spec)}\n\n"
        "## 5. Information Architecture\n\n"
        f"Seções: {_lista_md(ia.sections)}\n\n"
        f"Notas de navegação: {ia.navigation_notes or '(nenhuma)'}\n\n"
        f"## 6. Recomendações de Acessibilidade\n{_lista_md(spec.accessibility_recommendations)}\n\n"
        "## 7. User Journey\n\n"
        "> Não gerado por este agente. Referência à User Journey já existente no PRD de "
        "origem (Product Manager) — não disponível no PRD de origem, se não citado como "
        "contexto.\n\n"
        "## 8. Wireframes\n\n"
        "> Fora de escopo nesta fase. Responsabilidade planejada do futuro agente irmão "
        "AQuA-QE UI Designer.\n\n"
        "## 9. Protótipos\n\n"
        "> Fora de escopo nesta fase, mesma razão da seção 8.\n\n"
        f"## 10. Regras de Usabilidade\n{_lista_md(spec.review_notes)}\n\n"
        "## 11. Design System\n\n"
        "> Fora de escopo nesta fase, mesma razão da seção 8.\n\n"
        "## 12. Recomendações\n"
        f"{_lista_md(spec.accessibility_recommendations + spec.review_notes)}\n\n"
        f"## Rastreabilidade\n\n> {spec.source_reference}\n"
    )
