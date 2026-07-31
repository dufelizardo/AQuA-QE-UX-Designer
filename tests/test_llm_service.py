import pytest

from aqua_qe_ux_designer.services import llm_service


def test_generator_model_default(monkeypatch):
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    assert llm_service.generator_model() == "mistral"


def test_reviewer_model_default(monkeypatch):
    monkeypatch.delenv("OLLAMA_REVIEW_MODEL", raising=False)

    assert llm_service.reviewer_model() == "phi4"


def test_generator_model_respects_explicit_env(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "meu-modelo-customizado")

    assert llm_service.generator_model() == "meu-modelo-customizado"


def test_complete_json_dispatches_to_ollama(monkeypatch):
    captured = {}

    class FakeOllamaClient:
        def chat(self, model, messages, **kwargs):
            captured["model"] = model
            captured["messages"] = messages
            captured["kwargs"] = kwargs
            return {"message": {"content": '{"ok": true}'}}

    monkeypatch.setattr(llm_service, "_client", lambda: FakeOllamaClient())

    resultado = llm_service.complete_json("pergunta", system="sistema")

    assert resultado == {"ok": True}
    assert captured["model"] == "mistral"
    assert captured["kwargs"] == {"format": "json"}
    assert captured["messages"] == [
        {"role": "system", "content": "sistema"},
        {"role": "user", "content": "pergunta"},
    ]


def test_complete_dispatches_without_json_format(monkeypatch):
    captured = {}

    class FakeOllamaClient:
        def chat(self, model, messages, **kwargs):
            captured["kwargs"] = kwargs
            return {"message": {"content": "resposta em texto"}}

    monkeypatch.setattr(llm_service, "_client", lambda: FakeOllamaClient())

    resultado = llm_service.complete("pergunta")

    assert resultado == "resposta em texto"
    assert captured["kwargs"] == {}


def test_complete_json_raises_on_invalid_json(monkeypatch):
    class FakeOllamaClient:
        def chat(self, model, messages, **kwargs):
            return {"message": {"content": "isto não é json"}}

    monkeypatch.setattr(llm_service, "_client", lambda: FakeOllamaClient())

    with pytest.raises(ValueError):
        llm_service.complete_json("pergunta")


def test_complete_json_rejects_non_dict_json(monkeypatch):
    """Regressão: um agente irmão desta plataforma quebrou ao vivo quando o LLM devolveu uma
    lista JSON em vez de um objeto — complete_json deve rejeitar isso explicitamente."""

    class FakeOllamaClient:
        def chat(self, model, messages, **kwargs):
            return {"message": {"content": "[1, 2, 3]"}}

    monkeypatch.setattr(llm_service, "_client", lambda: FakeOllamaClient())

    with pytest.raises(ValueError):
        llm_service.complete_json("pergunta")


def test_complete_json_tolera_chaves_extras_apos_json_valido(monkeypatch):
    class FakeOllamaClient:
        def chat(self, model, messages, **kwargs):
            return {"message": {"content": '{"titulo": "Exemplo"}\n}\n}'}}

    monkeypatch.setattr(llm_service, "_client", lambda: FakeOllamaClient())

    resultado = llm_service.complete_json("pergunta")

    assert resultado == {"titulo": "Exemplo"}


def test_complete_json_ainda_rejeita_json_truncado(monkeypatch):
    class FakeOllamaClient:
        def chat(self, model, messages, **kwargs):
            return {"message": {"content": '{"titulo": "Exemplo", "itens": ["a", "b"'}}

    monkeypatch.setattr(llm_service, "_client", lambda: FakeOllamaClient())

    with pytest.raises(ValueError):
        llm_service.complete_json("pergunta")


def test_explicit_model_argument_overrides_generator_model(monkeypatch):
    captured = {}

    class FakeOllamaClient:
        def chat(self, model, messages, **kwargs):
            captured["model"] = model
            return {"message": {"content": '{"ok": true}'}}

    monkeypatch.setattr(llm_service, "_client", lambda: FakeOllamaClient())

    llm_service.complete_json("pergunta", model="modelo-especifico")

    assert captured["model"] == "modelo-especifico"
