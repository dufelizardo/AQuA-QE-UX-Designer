from ..models import InformationArchitecture
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você projeta o mapa de navegação/categorização (arquitetura da informação) para o "
    "escopo de um Épico, seguindo categorização por tarefa e profundidade razoável de "
    "navegação, e considerando a Lei de Miller/Carga Cognitiva (poucas categorias de alto "
    "nível, bem distintas entre si). Baseie-se apenas no texto informado; nunca invente uma "
    "seção sem lastro no Épico."
)


def design_information_architecture(texto_epic: str, contexto: dict) -> InformationArchitecture:
    """Gera o mapa de navegação/categorização do Épico, rastreável à fonte."""
    prompt = (
        f"Contexto: {contexto.get('context_problem', '')}\n"
        f"Épico:\n{texto_epic}\n\n"
        'Responda apenas em JSON: {"secoes": ["..."], "notas_navegacao": "...", '
        '"trecho_fonte": "..."}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return InformationArchitecture(
        sections=dados.get("secoes", []),
        navigation_notes=dados.get("notas_navegacao", ""),
        source_reference=dados.get("trecho_fonte", ""),
    )
