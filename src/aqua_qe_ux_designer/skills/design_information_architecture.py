from ..models import InformationArchitecture
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você projeta o mapa de navegação/categorização (arquitetura da informação) para o "
    "escopo de um Épico ou Story, seguindo categorização por tarefa e profundidade razoável "
    "de navegação, e considerando a Lei de Miller/Carga Cognitiva — gere entre 2 e 6 seções "
    "de alto nível, bem distintas entre si, nunca mais que isso.\n\n"
    "Uma 'seção' é o nome de uma área/tela/categoria de navegação (ex.: 'Agendamentos', "
    "'Meu Cadastro', 'Confirmação de Consulta') — nunca uma regra de negócio, um critério de "
    "aceitação ou uma frase copiada literalmente da fonte. Errado: transformar cada bullet de "
    "'Regras de Negócio' ou 'Critérios de Aceitação' em uma seção separada. Certo: agrupar o "
    "que essas regras/critérios descrevem em poucas categorias de navegação reais.\n\n"
    "Se a fonte for uma User Story única e específica (não um Épico com múltiplas áreas), é "
    "esperado ter poucas seções (às vezes só 1-2) — isso não é um erro; não infle a lista "
    "repetindo frases da Story como se fossem seções distintas.\n\n"
    "Baseie-se apenas no texto informado; nunca invente uma seção sem lastro na fonte. Cada "
    "seção deve ser uma única string de texto curta (ex.: 'Agendamentos: consulta e "
    "gerenciamento de horários'), nunca um objeto/dicionário com campos separados. O campo "
    "'trecho_fonte' deve ser um EXCERTO CURTO (uma frase, no máximo ~200 caracteres) do Épico "
    "que evidencia a arquitetura da informação — nunca o Épico inteiro nem o PRD completo."
)


def _secao_para_string(item) -> str:
    """Defesa contra o LLM devolver um objeto em vez de string para uma seção (ex.: {"nome": ..., "descricao": ...}),
    e contra marcadores de lista ("- "/"* ") embutidos no próprio texto da seção."""
    if isinstance(item, dict):
        nome = item.get("nome", "")
        descricao = item.get("descricao", "")
        texto = f"{nome}: {descricao}" if descricao else nome
    else:
        texto = str(item)
    return texto.lstrip("-* ").strip()


def design_information_architecture(texto_epic: str, contexto: dict) -> InformationArchitecture:
    """Gera o mapa de navegação/categorização do Épico, rastreável à fonte."""
    prompt = (
        f"Contexto: {contexto.get('context_problem', '')}\n"
        f"Épico:\n{texto_epic}\n\n"
        'Responda apenas em JSON, ex.: {"secoes": ["Agendamentos", "Confirmação de '
        'Consulta"], "notas_navegacao": "...", "trecho_fonte": "..."}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return InformationArchitecture(
        sections=[
            secao
            for item in dados.get("secoes", [])
            if (secao := _secao_para_string(item))
        ],
        navigation_notes=dados.get("notas_navegacao", ""),
        source_reference=dados.get("trecho_fonte", ""),
    )
