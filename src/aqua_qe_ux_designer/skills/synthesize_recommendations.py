from ..services.llm_service import complete_json

_SYSTEM = (
    "Você sintetiza e prioriza recomendações para o time de desenvolvimento/design "
    "considerar antes da implementação, a partir de duas listas já existentes: "
    "recomendações de acessibilidade (fundamentadas em WCAG 2.2) e observações de "
    "usabilidade (revisão heurística). Aponte as 3 a 5 questões mais críticas, combinando "
    "as duas listas por ordem de importância — nunca invente uma recomendação nova que não "
    "esteja em nenhuma das duas listas informadas; você só reordena/resume o que já existe, "
    "nunca cria conteúdo além disso. Cada item da síntese deve ser uma única string de "
    "texto, nunca um objeto/dicionário com campos separados. Responda sempre em português."
)


def _item_para_string(item) -> str:
    """Defesa contra o LLM devolver um objeto em vez de string para um item da síntese."""
    if isinstance(item, dict):
        valor = next((v for v in item.values() if v), "")
        return str(valor) if valor else str(item)
    return str(item)


def synthesize_recommendations(
    accessibility_recommendations: list[str], review_notes: list[str]
) -> list[str]:
    """Sintetiza/prioriza as recomendações de acessibilidade e as observações de usabilidade já existentes, sem inventar itens novos."""
    if not accessibility_recommendations and not review_notes:
        return []
    prompt = (
        f"Recomendações de acessibilidade:\n{accessibility_recommendations}\n\n"
        f"Observações de usabilidade:\n{review_notes}\n\n"
        'Responda apenas em JSON: {"sintese": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return [_item_para_string(item) for item in dados.get("sintese", [])]
