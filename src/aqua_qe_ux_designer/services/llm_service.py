import json
import os

import ollama

_DEFAULT_MODEL = "mistral"
_DEFAULT_REVIEW_MODEL = "phi4"


def _client() -> ollama.Client:
    host = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return ollama.Client(host=host)


def generator_model() -> str:
    """Resolve o modelo gerador (Ollama local — sem piloto de provedor em nuvem nesta fase, ver CLAUDE.md)."""
    return os.getenv("OLLAMA_MODEL", _DEFAULT_MODEL)


def reviewer_model() -> str:
    """Resolve o modelo revisor (Ollama local, sempre diferente do gerador — mitiga self-preference bias)."""
    return os.getenv("OLLAMA_REVIEW_MODEL", _DEFAULT_REVIEW_MODEL)


def _chat(modelo: str, messages: list[dict], json_mode: bool) -> str:
    kwargs = {"format": "json"} if json_mode else {}
    resposta = _client().chat(model=modelo, messages=messages, **kwargs)
    return resposta["message"]["content"]


def complete(prompt: str, system: str = "", model: str | None = None) -> str:
    """Envia um prompt ao Ollama local e retorna o texto de resposta."""
    modelo = model or generator_model()
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    return _chat(modelo, messages, json_mode=False)


def complete_json(prompt: str, system: str = "", model: str | None = None) -> dict:
    """Envia um prompt ao Ollama local e retorna a resposta já parseada como JSON.

    Usa `raw_decode` em vez de `json.loads` — aceita o primeiro objeto JSON válido e ignora
    qualquer lixo depois dele (mesmo achado ao vivo já documentado nos agentes irmãos).
    Rejeita explicitamente qualquer JSON que não seja um objeto (ex.: uma lista bruta), erro
    real já visto em outro agente irmão desta plataforma.
    """
    modelo = model or generator_model()
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    conteudo = _chat(modelo, messages, json_mode=True)
    try:
        dados, _ = json.JSONDecoder().raw_decode(conteudo.strip())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Resposta do LLM não é um JSON válido: {conteudo!r}") from exc
    if not isinstance(dados, dict):
        raise ValueError(f"Resposta do LLM não é um objeto JSON: {conteudo!r}")
    return dados
