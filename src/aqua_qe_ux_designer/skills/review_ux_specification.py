from ..models import UXSpecification
from ..services.llm_service import complete_json, reviewer_model

_SYSTEM = (
    "Você é um revisor heurístico de UX Specifications, independente de quem as gerou. "
    "Avalie os fluxos de navegação e a arquitetura da informação contra as 10 Heurísticas de "
    "Nielsen e as Laws of UX (Hick, Jakob, Miller, Carga Cognitiva). Esta é sempre uma "
    "avaliação de especialista, nunca um teste com usuário real — nunca escreva como se "
    "usuários reais tivessem sido observados (GR-UX-3). Aponte problemas reais; nunca aprove "
    "algo com justificativa vaga."
)


def review_ux_specification(spec: UXSpecification) -> dict:
    """Revisa a UX Specification com um LLM diferente do gerador, fundamentado nas heurísticas de Nielsen e nas Laws of UX — sempre avaliação de especialista, nunca teste real (GR-UX-3)."""
    modelo = reviewer_model()
    fluxos = [{"nome": f.name, "passos": f.steps} for f in spec.user_flows]
    prompt = (
        f"Título: {spec.title}\n"
        f"Contexto: {spec.context_problem}\n"
        f"Fluxos de usuário: {fluxos}\n"
        f"Arquitetura da informação: {spec.information_architecture.sections}\n"
        f"Notas de navegação: {spec.information_architecture.navigation_notes}\n"
        f"Recomendações de acessibilidade: {spec.accessibility_recommendations}\n\n"
        'Responda apenas em JSON: {"aprovado": true ou false, "problemas": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM, model=modelo)
    return {
        "aprovado": bool(dados.get("aprovado", False)),
        "problemas": dados.get("problemas", []),
    }
