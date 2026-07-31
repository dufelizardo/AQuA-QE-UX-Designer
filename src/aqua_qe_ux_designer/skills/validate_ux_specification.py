from ..models import UXSpecification


def validate_ux_specification(spec: UXSpecification) -> list[str]:
    """Valida a UX Specification contra o checklist automático e retorna os motivos de reprovação (lista vazia = aprovado no checklist)."""
    motivos = []
    if not spec.title:
        motivos.append("título ausente")
    if not spec.context_problem:
        motivos.append("contexto do problema ausente")
    if not spec.user_flows:
        motivos.append("nenhum fluxo de usuário identificado")
    else:
        for fluxo in spec.user_flows:
            if len(fluxo.steps) < 2:
                motivos.append(f"fluxo '{fluxo.name}' tem menos de 2 passos")
    if not spec.information_architecture.sections:
        motivos.append("arquitetura da informação sem seções")
    if not spec.accessibility_recommendations:
        motivos.append("nenhuma recomendação de acessibilidade")
    if not spec.personas_reference:
        motivos.append(
            "Personas não identificadas no PRD de origem — "
            "necessário esclarecer quem são os usuários desta funcionalidade (GR-UX-4)"
        )
    if not spec.journey_reference:
        motivos.append(
            "User Journey não identificada no PRD de origem — "
            "necessário esclarecer qual a jornada do usuário para esta tarefa (GR-UX-4)"
        )
    return motivos
