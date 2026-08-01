import ast

from ..services.llm_service import complete_json

_SYSTEM = (
    "Responda sempre em português.\n\n"
    "Você extrai um título curto e um resumo do problema/contexto de uma tarefa a partir de "
    "um PRD e de uma Story/Epic associados. O resumo do contexto deve se basear no que a "
    "Story/Epic realmente descreve; nunca afirme que algo é 'fora de escopo' do PRD (ou "
    "qualquer outra atribuição ao PRD) a menos que você consiga apontar exatamente onde o "
    "PRD diz isso — na dúvida, descreva só o que a Story pede, sem caracterizar o "
    "posicionamento do PRD sobre o assunto.\n\n"
    "Identifique também, separadamente, se existirem no PRD:\n"
    "(1) trechos da seção **'Personas'** relevantes à tarefa — se houver mais de uma Persona "
    "relevante (ex.: o cidadão E o agente de saúde que executa a tarefa em seu nome), cite "
    "**todas**, cada uma com Descrição/Objetivos/Pontos de dor tal como aparecem no PRD. "
    "Nunca reduza a uma única frase genérica quando o PRD tem conteúdo estruturado "
    "disponível.\n"
    "(2) trechos da seção **'Jornadas do Usuário'** (User Journey) relevantes à tarefa — a "
    "jornada é a sequência de passos que uma persona percorre ao longo do tempo para atingir "
    "um objetivo. Cite o nome da jornada e seus passos tal como aparecem no PRD, sem misturar "
    "detalhes de outras fontes (Story, critérios de aceitação) que não façam parte da jornada "
    "no PRD. **Nunca confunda com a seção 'Casos de Uso'** — Caso de Uso é uma interação "
    "pontual entre ator e sistema, um conceito diferente de User Journey; se só existir 'Casos "
    "de Uso' e não existir 'Jornadas do Usuário' no PRD, responda com string vazia para a "
    "jornada, nunca use o conteúdo de Casos de Uso como substituto.\n\n"
    "Cite os trechos **literalmente** (copie o texto do PRD, não parafraseie nem resuma em "
    "uma frase própria), em prosa legível — frases completas separadas por quebra de linha, "
    "nunca no formato \"Nome: 'descrição'\" (estilo dicionário serializado). Os campos "
    "'personas' e 'jornada_usuario' devem sempre ser uma única string de texto, nunca uma "
    "lista/array JSON, mesmo quando o conteúdo tem múltiplos itens — nesse caso, junte os "
    "itens na mesma string, um por linha. Nunca crie uma Persona ou Journey nova (essas "
    "seções já existem no PRD do Product Manager, GR-UX-4). Se o PRD não tiver a seção "
    "correspondente, responda com string vazia — nunca invente uma para preencher a lacuna. "
    "Baseie-se apenas no texto informado; nunca invente contexto que não esteja lá."
)


def _item_para_string(item) -> str:
    """Defesa contra o LLM devolver um objeto em vez de string para um item de personas/jornada
    (ex.: {"nome": ..., "descricao": ...})."""
    if isinstance(item, dict):
        nome = item.get("nome", "")
        descricao = item.get("descricao", "")
        return f"{nome}: {descricao}" if descricao else (nome or str(item))
    return str(item)


def _valor_para_string(valor) -> str:
    """Achata um valor (string, lista ou dict aninhado) numa string legível de uma linha —
    usado para os valores dentro de um dict de personas/jornada (ver `_dict_para_texto`)."""
    if isinstance(valor, dict):
        partes = [f"{chave}: {_valor_para_string(sub)}" for chave, sub in valor.items() if sub]
        return "; ".join(partes)
    if isinstance(valor, list):
        return ", ".join(_item_para_string(item) for item in valor)
    return str(valor) if valor else ""


def _dict_para_texto(dicionario: dict) -> str:
    """Achata um dict devolvido no lugar de uma string de personas/jornada — cobre um dict de
    nome->detalhes (ex.: personas por nome, com sub-dict de descrição/objetivos), um dict de
    passo->'' (ex.: jornada com cada passo como chave e valor vazio), e um dict com uma única
    chave-artefato mapeando para a lista de passos (ex.: {"caminho": [...]}, achado ao vivo) —
    nesse último caso a chave não tem valor de rótulo real, então é descartada."""
    if len(dicionario) == 1:
        ((unica_chave, unico_valor),) = dicionario.items()
        if isinstance(unico_valor, list):
            return "\n".join(_item_para_string(item) for item in unico_valor)
    linhas = []
    for chave, valor in dicionario.items():
        detalhe = _valor_para_string(valor)
        linhas.append(f"{chave}: {detalhe}" if detalhe else str(chave))
    return "\n".join(linhas)


def _string_como_estrutura(valor: str):
    """Defesa contra o LLM devolver uma string cujo próprio conteúdo é um repr de dict/list
    Python (aspas simples, ex.: "{'Cidadãos': {'descricao': ...}}") em vez de prosa — achado ao
    vivo (Groq/llama-3.3-70b-versatile): o campo chega como string (não como objeto/array JSON),
    então as checagens de isinstance(dict)/isinstance(list) abaixo não disparam sozinhas."""
    texto = valor.strip()
    if not texto or texto[0] not in "{[":
        return None
    try:
        estrutura = ast.literal_eval(texto)
    except (ValueError, SyntaxError):
        return None
    return estrutura if isinstance(estrutura, (dict, list)) else None


def _texto_ou_lista(valor) -> str:
    """Defesa contra o LLM devolver uma lista, um dict, ou uma string com repr de dict/list
    (em formatos variados, achados ao vivo em execuções diferentes) em vez de uma única string
    de prosa para personas/jornada."""
    if isinstance(valor, dict):
        return _dict_para_texto(valor)
    if isinstance(valor, list):
        return "\n".join(_item_para_string(item) for item in valor)
    if isinstance(valor, str):
        estrutura = _string_como_estrutura(valor)
        if estrutura is not None:
            return _texto_ou_lista(estrutura)
    return valor or ""


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
        "personas_reference": _texto_ou_lista(dados.get("personas", "")),
        "journey_reference": _texto_ou_lista(dados.get("jornada_usuario", "")),
    }
