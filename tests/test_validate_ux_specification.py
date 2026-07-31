from aqua_qe_ux_designer.models import InformationArchitecture, UserFlow, UXSpecification
from aqua_qe_ux_designer.skills.validate_ux_specification import validate_ux_specification


def _spec_completa(**overrides) -> UXSpecification:
    base = {
        "id": "UX-001",
        "title": "titulo",
        "context_problem": "contexto",
        "user_flows": [UserFlow(name="f", steps=["passo 1", "passo 2"], source_reference="fonte")],
        "information_architecture": InformationArchitecture(sections=["Home"]),
        "accessibility_recommendations": ["recomendar a verificar contraste"],
    }
    base.update(overrides)
    return UXSpecification(**base)


def test_valid_ux_specification_passes():
    assert validate_ux_specification(_spec_completa()) == []


def test_missing_title_fails():
    assert "título ausente" in validate_ux_specification(_spec_completa(title=""))


def test_missing_context_fails():
    assert "contexto do problema ausente" in validate_ux_specification(_spec_completa(context_problem=""))


def test_no_user_flows_fails():
    motivos = validate_ux_specification(_spec_completa(user_flows=[]))
    assert "nenhum fluxo de usuário identificado" in motivos


def test_flow_with_single_step_fails():
    motivos = validate_ux_specification(
        _spec_completa(user_flows=[UserFlow(name="f", steps=["único passo"], source_reference="x")])
    )
    assert "fluxo 'f' tem menos de 2 passos" in motivos


def test_empty_information_architecture_fails():
    motivos = validate_ux_specification(
        _spec_completa(information_architecture=InformationArchitecture())
    )
    assert "arquitetura da informação sem seções" in motivos


def test_no_accessibility_recommendations_fails():
    motivos = validate_ux_specification(_spec_completa(accessibility_recommendations=[]))
    assert "nenhuma recomendação de acessibilidade" in motivos


def test_multiplos_motivos_acumulam_em_vez_de_parar_no_primeiro():
    motivos = validate_ux_specification(_spec_completa(title="", accessibility_recommendations=[]))
    assert "título ausente" in motivos
    assert "nenhuma recomendação de acessibilidade" in motivos
