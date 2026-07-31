from ..services.llm_service import complete_json

_SYSTEM = (
    "Você extrai um título curto e um resumo do problema/contexto de uma tarefa a partir de "
    "um PRD e de uma Story/Epic associados. Identifique também, separadamente, se existirem "
    "no PRD: (1) trechos de Personas relevantes à tarefa, e (2) trechos de User Journey "
    "relevantes à tarefa — cite-os literalmente, nunca crie uma Persona ou Journey nova "
    "(essas seções já existem no PRD do Product Manager, GR-UX-4). Se o PRD não tiver uma "
    "seção de Personas, ou não tiver uma seção de User Journey, responda com string vazia "
    "para o campo correspondente — nunca invente uma para preencher a lacuna. Baseie-se "
    "apenas no texto informado; nunca invente contexto que não esteja lá."
)


def extract_ux_context(texto_prd: str, texto_story_ou_epic: str) -> dict:
    """Extrai título e contexto do problema a partir do PRD + Story/Epic; repassa Personas e User Journey já existentes no PRD como contexto (separadamente), nunca as regenera (GR-UX-4)."""
    prompt = (
        f"PRD:\n{texto_prd}\n\n"
        f"Story/Epic:\n{texto_story_ou_epic}\n\n"
        'Responda apenas em JSON: {"titulo": "...", "contexto": "...", '
        '"personas": "...", "jornada_usuario": "..."}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return {
        "title": dados.get("titulo", ""),
        "context_problem": dados.get("contexto", ""),
        "personas_reference": dados.get("personas", ""),
        "journey_reference": dados.get("jornada_usuario", ""),
    }
