from aqua_qe_ux_designer.models import InformationArchitecture, UserFlow, UXSpecification
from aqua_qe_ux_designer.skills.format_ux_specification_markdown import (
    format_ux_specification_markdown,
)


def test_format_ux_specification_markdown_includes_all_fields():
    spec = UXSpecification(
        id="UX-001",
        title="Agendamento de Consulta",
        context_problem="Paciente precisa agendar uma consulta pelo app",
        user_flows=[
            UserFlow(
                name="Agendamento assistido",
                steps=["abrir tela de agendamento", "escolher horário", "confirmar"],
                source_reference="trecho 1",
            )
        ],
        information_architecture=InformationArchitecture(
            sections=["Início", "Agendamentos"], navigation_notes="Agendamentos acessível pela home"
        ),
        accessibility_recommendations=["verificar contraste (WCAG 1.4.3)"],
        source_reference="texto fonte completo",
        review_notes=["fluxo sem confirmação visual explícita"],
    )

    resultado = format_ux_specification_markdown(spec)

    assert "# Agendamento de Consulta" in resultado
    assert "**ID**: UX-001" in resultado
    assert "**Status**: pending_clarification" in resultado
    assert "Paciente precisa agendar uma consulta pelo app" in resultado
    assert "### Agendamento assistido" in resultado
    assert "1. abrir tela de agendamento" in resultado
    assert "2. escolher horário" in resultado
    assert "3. confirmar" in resultado
    assert "Seções: - Início\n- Agendamentos" in resultado
    assert "Agendamentos acessível pela home" in resultado
    assert "- verificar contraste (WCAG 1.4.3)" in resultado
    assert "- fluxo sem confirmação visual explícita" in resultado
    assert "> texto fonte completo" in resultado
    assert "Fora de escopo nesta fase" in resultado
    assert "Não gerado por este agente" in resultado


def test_format_ux_specification_markdown_omits_empty_sections_gracefully():
    spec = UXSpecification(id="UX-002", title="t", context_problem="c")

    resultado = format_ux_specification_markdown(spec)

    assert "(nenhum)" in resultado
    assert "(nenhuma)" in resultado
