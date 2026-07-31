from ..models import UXSpecification
from ..services.llm_service import complete_json, reviewer_model

_SYSTEM = (
    "Você é um revisor heurístico de UX Specifications, independente de quem as gerou. "
    "Avalie os fluxos de navegação e a arquitetura da informação contra as 10 Heurísticas de "
    "Nielsen e as Laws of UX (Hick, Jakob, Miller, Carga Cognitiva). Esta é sempre uma "
    "avaliação de especialista, nunca um teste com usuário real — nunca escreva como se "
    "usuários reais tivessem sido observados (GR-UX-3). Aponte problemas reais; nunca aprove "
    "algo com justificativa vaga. Cada problema apontado deve ser uma única string de texto "
    "(ex.: 'Visibilidade do status do sistema: o fluxo não informa o usuário após cada "
    "etapa'), nunca um objeto/dicionário com campos separados."
)


def _problema_para_string(item) -> str:
    """Defesa contra o LLM devolver um objeto em vez de string para um problema apontado
    (ex.: {"heuristica_de_nielsen": ..., "detalhes": ..., "recomendacao": ...})."""
    if isinstance(item, dict):
        detalhes = item.get("detalhes", "")
        recomendacao = item.get("recomendacao") or item.get("recomendação", "")
        topico = next(
            (
                valor
                for chave, valor in item.items()
                if chave not in ("detalhes", "recomendacao", "recomendação") and valor
            ),
            "",
        )
        partes = [parte for parte in (topico, detalhes, recomendacao) if parte]
        return " — ".join(partes) if partes else str(item)
    return str(item)


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
        "problemas": [_problema_para_string(item) for item in dados.get("problemas", [])],
    }
