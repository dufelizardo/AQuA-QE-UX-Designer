from ..models import UserFlow
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você identifica o fluxo de navegação concreto (sequência de passos/telas) necessário "
    "para completar a tarefa descrita em uma User Story, sempre rastreável ao texto de "
    "origem — nunca invente um passo sem base real na Story (GR-UX-1). Organize os passos "
    "considerando a Lei de Hick (menos opções por tela facilitam a decisão) e a Lei de Jakob "
    "(siga padrões de navegação já conhecidos do usuário), nunca como justificativa para "
    "adicionar um passo sem lastro na Story. Se a Story não tiver informação suficiente para "
    "um fluxo completo, retorne poucos passos em vez de inventar o restante. Cada passo deve "
    "ser uma única string de texto, nunca um objeto/dicionário com campos separados. O campo "
    "'trecho_fonte' deve ser um EXCERTO CURTO (uma frase, no máximo ~200 caracteres) da Story "
    "que evidencia o fluxo — nunca a Story inteira nem o PRD completo."
)


def _passo_para_string(item) -> str:
    """Defesa contra o LLM devolver um objeto em vez de string para um passo (ex.: {"passo": ..., "trecho_fonte": ...})."""
    if isinstance(item, dict):
        return item.get("passo") or item.get("nome") or str(item)
    return str(item)


def identify_user_flows(texto_story: str, contexto: dict) -> UserFlow:
    """Identifica o fluxo de navegação concreto para a tarefa da Story, rastreável à fonte (GR-UX-1)."""
    prompt = (
        f"Contexto: {contexto.get('context_problem', '')}\n"
        f"Story:\n{texto_story}\n\n"
        'Responda apenas em JSON: {"nome": "...", "passos": ["..."], "trecho_fonte": "..."}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return UserFlow(
        name=dados.get("nome", ""),
        steps=[_passo_para_string(item) for item in dados.get("passos", [])],
        source_reference=dados.get("trecho_fonte", ""),
    )
