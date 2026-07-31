from aqua_qe_ux_designer.models import UXSpecification
from aqua_qe_ux_designer.orchestrator import ux_designer as module


def test_handle_request_delegates_to_workflow(monkeypatch):
    esperado = UXSpecification(id="UX-001", title="t", context_problem="c")
    captured = {}

    def fake_generate(texto_prd, texto_ticket, prd_reference, ticket_reference):
        captured["texto_prd"] = texto_prd
        captured["texto_ticket"] = texto_ticket
        captured["prd_reference"] = prd_reference
        captured["ticket_reference"] = ticket_reference
        return esperado

    monkeypatch.setattr(module, "generate_ux_specification", fake_generate)

    resultado = module.handle_request("prd", "ticket", "url-prd", "AQUAQE-11")

    assert resultado is esperado
    assert captured == {
        "texto_prd": "prd",
        "texto_ticket": "ticket",
        "prd_reference": "url-prd",
        "ticket_reference": "AQUAQE-11",
    }
