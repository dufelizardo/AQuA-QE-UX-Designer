from aqua_qe_ux_designer.models import (
    ArtifactStatus,
    InformationArchitecture,
    UserFlow,
    UXSpecification,
)


def test_user_flow_defaults():
    fluxo = UserFlow(name="Agendamento")
    assert fluxo.steps == []
    assert fluxo.source_reference == ""


def test_information_architecture_defaults():
    ia = InformationArchitecture()
    assert ia.sections == []
    assert ia.navigation_notes == ""


def test_ux_specification_defaults_to_pending_clarification():
    spec = UXSpecification(id="UX-001", title="t", context_problem="c")
    assert spec.status == ArtifactStatus.PENDING_CLARIFICATION
    assert spec.user_flows == []
    assert isinstance(spec.information_architecture, InformationArchitecture)
    assert spec.accessibility_recommendations == []
    assert spec.review_notes == []
    assert spec.prd_reference == ""
    assert spec.ticket_reference == ""
    assert spec.personas_reference == ""
    assert spec.journey_reference == ""
    assert spec.recommendations_synthesis == []


def test_ux_specification_accepts_full_payload():
    spec = UXSpecification(
        id="UX-001",
        title="t",
        context_problem="c",
        user_flows=[UserFlow(name="f", steps=["passo 1", "passo 2"], source_reference="fonte")],
        information_architecture=InformationArchitecture(sections=["Home"], navigation_notes="n"),
        accessibility_recommendations=["verificar contraste"],
        source_reference="fonte completa",
        prd_reference="https://example.atlassian.net/wiki/pages/1",
        ticket_reference="AQUAQE-11",
        personas_reference="Persona: Cidadão",
        journey_reference="Jornada: agenda consulta",
        recommendations_synthesis=["priorizar validação em tempo real"],
        status=ArtifactStatus.DRAFT_VALIDATED,
        review_notes=["nota"],
    )
    assert spec.user_flows[0].name == "f"
    assert spec.information_architecture.sections == ["Home"]
    assert spec.status == ArtifactStatus.DRAFT_VALIDATED
    assert spec.prd_reference == "https://example.atlassian.net/wiki/pages/1"
    assert spec.ticket_reference == "AQUAQE-11"
    assert spec.personas_reference == "Persona: Cidadão"
    assert spec.journey_reference == "Jornada: agenda consulta"
    assert spec.recommendations_synthesis == ["priorizar validação em tempo real"]
