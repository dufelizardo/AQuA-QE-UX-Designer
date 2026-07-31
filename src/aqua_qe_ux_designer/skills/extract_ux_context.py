from ..services.llm_service import complete_json

_SYSTEM = (
    "Você extrai um título curto e um resumo do problema/contexto de uma tarefa a partir de "
    "um PRD e de uma Story/Epic associados. Identifique também, se existirem no PRD, trechos "
    "de Personas e User Journey relevantes à tarefa — cite-os literalmente, nunca crie uma "
    "Persona ou Journey nova (essas seções já existem no PRD do Product Manager, GR-UX-4). "
    "Baseie-se apenas no texto informado; nunca invente contexto que não esteja lá."
)


def extract_ux_context(texto_prd: str, texto_story_ou_epic: str) -> dict:
    """Extrai título e contexto do problema a partir do PRD + Story/Epic; repassa Personas/User Journey já existentes no PRD como contexto, nunca as regenera (GR-UX-4)."""
    prompt = (
        f"PRD:\n{texto_prd}\n\n"
        f"Story/Epic:\n{texto_story_ou_epic}\n\n"
        'Responda apenas em JSON: {"titulo": "...", "contexto": "...", '
        '"personas_journeys": "..."}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return {
        "title": dados.get("titulo", ""),
        "context_problem": dados.get("contexto", ""),
        "personas_journeys": dados.get("personas_journeys", ""),
    }
