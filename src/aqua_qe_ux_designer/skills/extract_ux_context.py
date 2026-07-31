from ..services.llm_service import complete_json

_SYSTEM = (
    "Você extrai um título curto e um resumo do problema/contexto de uma tarefa a partir de "
    "um PRD e de uma Story/Epic associados. Identifique também, separadamente, se existirem "
    "no PRD:\n"
    "(1) trechos da seção **'Personas'** relevantes à tarefa;\n"
    "(2) trechos da seção **'Jornadas do Usuário'** (User Journey) relevantes à tarefa — a "
    "jornada é a sequência de passos que uma persona percorre ao longo do tempo para atingir "
    "um objetivo. **Nunca confunda com a seção 'Casos de Uso'** — Caso de Uso é uma interação "
    "pontual entre ator e sistema, um conceito diferente de User Journey; se só existir 'Casos "
    "de Uso' e não existir 'Jornadas do Usuário' no PRD, responda com string vazia para a "
    "jornada, nunca use o conteúdo de Casos de Uso como substituto.\n\n"
    "Cite os trechos literalmente, em prosa legível (frases completas ou lista com '- '), "
    "nunca no formato \"Nome: 'descrição'\" (estilo dicionário serializado). Nunca crie uma "
    "Persona ou Journey nova (essas seções já existem no PRD do Product Manager, GR-UX-4). Se "
    "o PRD não tiver a seção correspondente, responda com string vazia — nunca invente uma "
    "para preencher a lacuna. Baseie-se apenas no texto informado; nunca invente contexto que "
    "não esteja lá."
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
