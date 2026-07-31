from aqua_qe_ux_designer.models import (
    ArtifactStatus,
    InformationArchitecture,
    UserFlow,
    UXSpecification,
)
from aqua_qe_ux_designer.workflow import generate_ux_specification as workflow_module


def _stub_geracao(monkeypatch, com_ia_sections=True, com_acessibilidade=True, com_personas=True):
    monkeypatch.setattr(
        workflow_module,
        "extract_ux_context",
        lambda texto_prd, texto_ticket: {
            "title": "titulo",
            "context_problem": "contexto",
            "personas_reference": "Persona: Cidadão" if com_personas else "",
            "journey_reference": "Jornada: agenda consulta" if com_personas else "",
        },
    )
    monkeypatch.setattr(
        workflow_module,
        "identify_user_flows",
        lambda texto_ticket, contexto: UserFlow(
            name="fluxo", steps=["passo 1", "passo 2"], source_reference="f"
        ),
    )
    monkeypatch.setattr(
        workflow_module,
        "design_information_architecture",
        lambda texto_ticket, contexto: InformationArchitecture(
            sections=["Início"] if com_ia_sections else [], source_reference="f"
        ),
    )
    monkeypatch.setattr(
        workflow_module,
        "review_accessibility",
        lambda fluxo, ia: (["verificar contraste"] if com_acessibilidade else []),
    )


def test_generate_ux_specification_happy_path_marks_draft_validated_when_review_approves(
    monkeypatch,
):
    _stub_geracao(monkeypatch)
    monkeypatch.setattr(
        workflow_module, "review_ux_specification", lambda spec: {"aprovado": True, "problemas": []}
    )

    spec = workflow_module.generate_ux_specification(
        "prd", "ticket", prd_reference="https://example.atlassian.net/wiki/pages/1", ticket_reference="AQUAQE-11"
    )

    assert spec.status == ArtifactStatus.DRAFT_VALIDATED
    assert spec.title == "titulo"
    assert spec.user_flows[0].name == "fluxo"
    assert spec.information_architecture.sections == ["Início"]
    assert spec.accessibility_recommendations == ["verificar contraste"]
    assert spec.review_notes == []
    assert spec.prd_reference == "https://example.atlassian.net/wiki/pages/1"
    assert spec.ticket_reference == "AQUAQE-11"
    assert spec.personas_reference == "Persona: Cidadão"
    assert spec.journey_reference == "Jornada: agenda consulta"


def test_generate_ux_specification_missing_personas_marks_pending_clarification(monkeypatch):
    """GR-UX-4: sem Personas/Journey no PRD, reprova até o esclarecimento humano suprir a lacuna."""
    _stub_geracao(monkeypatch, com_personas=False)
    chamou_review = {"valor": False}

    def fake_review(spec):
        chamou_review["valor"] = True
        return {"aprovado": True, "problemas": []}

    monkeypatch.setattr(workflow_module, "review_ux_specification", fake_review)

    spec = workflow_module.generate_ux_specification("prd", "ticket")

    assert spec.status == ArtifactStatus.PENDING_CLARIFICATION
    assert chamou_review["valor"] is False
    assert any("Personas não identificadas" in nota for nota in spec.review_notes)
    assert any("User Journey não identificada" in nota for nota in spec.review_notes)


def test_generate_ux_specification_review_rejection_marks_pending_clarification(monkeypatch):
    _stub_geracao(monkeypatch)
    monkeypatch.setattr(
        workflow_module,
        "review_ux_specification",
        lambda spec: {"aprovado": False, "problemas": ["fluxo pouco claro"]},
    )

    spec = workflow_module.generate_ux_specification("prd", "ticket")

    assert spec.status == ArtifactStatus.PENDING_CLARIFICATION
    assert spec.review_notes == ["fluxo pouco claro"]


def test_generate_ux_specification_validate_failure_skips_review(monkeypatch):
    """Sem seções de IA nem acessibilidade, validate_ux_specification reprova antes de chamar o revisor."""
    _stub_geracao(monkeypatch, com_ia_sections=False, com_acessibilidade=False)
    chamou_review = {"valor": False}

    def fake_review(spec):
        chamou_review["valor"] = True
        return {"aprovado": True, "problemas": []}

    monkeypatch.setattr(workflow_module, "review_ux_specification", fake_review)

    spec = workflow_module.generate_ux_specification("prd", "ticket")

    assert spec.status == ArtifactStatus.PENDING_CLARIFICATION
    assert chamou_review["valor"] is False
    assert "arquitetura da informação sem seções" in spec.review_notes
    assert "nenhuma recomendação de acessibilidade" in spec.review_notes


def _spec_completa() -> UXSpecification:
    return UXSpecification(
        id="UX-001",
        title="t",
        context_problem="c",
        user_flows=[UserFlow(name="f", steps=["passo 1", "passo 2"], source_reference="f")],
        information_architecture=InformationArchitecture(sections=["Início"]),
        accessibility_recommendations=["verificar contraste"],
    )


def test_finalize_ux_specification_marca_pending_clarification_quando_validate_falha(monkeypatch):
    monkeypatch.setattr(workflow_module, "validate_ux_specification", lambda spec: ["título ausente"])

    spec = UXSpecification(id="UX-001", title="", context_problem="")
    resultado = workflow_module.finalize_ux_specification(spec)

    assert resultado.status == ArtifactStatus.PENDING_CLARIFICATION
    assert resultado.review_notes == ["título ausente"]


def test_finalize_ux_specification_marca_draft_validated_quando_tudo_aprova(monkeypatch):
    monkeypatch.setattr(workflow_module, "validate_ux_specification", lambda spec: [])
    monkeypatch.setattr(
        workflow_module, "review_ux_specification", lambda spec: {"aprovado": True, "problemas": []}
    )

    resultado = workflow_module.finalize_ux_specification(_spec_completa())

    assert resultado.status == ArtifactStatus.DRAFT_VALIDATED


def test_refine_and_finalize_ux_specification_revalida_e_revisa_apos_o_refino(monkeypatch):
    """Regressão (mesmo bug real já corrigido nos agentes irmãos): refinar sem revalidar deixaria status/review_notes obsoletos para sempre."""
    spec = UXSpecification(
        id="UX-001",
        title="t",
        context_problem="c",
        review_notes=["arquitetura da informação sem seções"],
    )
    monkeypatch.setattr(
        workflow_module,
        "_refinar_campos",
        lambda spec, respostas: _spec_completa(),
    )
    monkeypatch.setattr(workflow_module, "validate_ux_specification", lambda spec: [])
    monkeypatch.setattr(
        workflow_module, "review_ux_specification", lambda spec: {"aprovado": True, "problemas": []}
    )

    resultado = workflow_module.refine_and_finalize_ux_specification(
        spec, [{"pergunta": "p", "resposta": "r"}]
    )

    assert resultado.status == ArtifactStatus.DRAFT_VALIDATED
    assert resultado.review_notes == []
