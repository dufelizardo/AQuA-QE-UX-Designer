from ..models import InformationArchitecture, UserFlow
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você gera recomendações de acessibilidade fundamentadas em WCAG 2.2 sobre um fluxo de "
    "navegação e uma arquitetura da informação. Cada recomendação deve citar um critério "
    "WCAG 2.2 específico (ex.: '2.4.3 Ordem de Foco') e ser sempre redigida como algo 'a "
    "verificar' pela equipe de desenvolvimento — nunca como afirmação de conformidade "
    "(GR-UX-2). Nunca certifique que algo 'está em conformidade'."
)


def review_accessibility(
    user_flow: UserFlow, information_architecture: InformationArchitecture
) -> list[str]:
    """Gera recomendações de acessibilidade fundamentadas em WCAG 2.2, sempre 'a verificar', nunca certificação (GR-UX-2)."""
    prompt = (
        f"Fluxo de navegação: {user_flow.name}\nPassos: {user_flow.steps}\n\n"
        f"Arquitetura da informação: {information_architecture.sections}\n"
        f"Notas de navegação: {information_architecture.navigation_notes}\n\n"
        'Responda apenas em JSON: {"recomendacoes": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return dados.get("recomendacoes", [])
