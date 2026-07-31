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
            sections=["Início", "Agendamentos"],
            navigation_notes="Agendamentos acessível pela home",
            source_reference="trecho 2",
        ),
        accessibility_recommendations=["verificar contraste (WCAG 1.4.3)"],
        source_reference="texto fonte completo",
        prd_reference="https://example.atlassian.net/wiki/pages/1179649/PRD",
        ticket_reference="AQUAQE-11",
        personas_reference="Cidadãos que buscam atendimento presencial",
        journey_reference="Cidadão vai à unidade e agenda com auxílio de um agente",
        review_notes=[
            "Visibilidade do status do sistema — o fluxo não informa o usuário após cada etapa"
        ],
    )

    resultado = format_ux_specification_markdown(spec)

    assert "# Agendamento de Consulta" in resultado
    assert "**ID**: UX-001" in resultado
    assert "**Status**: pending_clarification" in resultado
    assert "Paciente precisa agendar uma consulta pelo app" in resultado
    assert "**PRD de origem**: https://example.atlassian.net/wiki/pages/1179649/PRD" in resultado
    assert "**Story/Epic de origem**: AQUAQE-11" in resultado
    assert "Cidadãos que buscam atendimento presencial" in resultado
    assert "Cidadão vai à unidade e agenda com auxílio de um agente" in resultado
    assert "### Agendamento assistido" in resultado
    assert "1. abrir tela de agendamento" in resultado
    assert "2. escolher horário" in resultado
    assert "3. confirmar" in resultado
    assert "Seções: - Início\n- Agendamentos" in resultado
    assert "Agendamentos acessível pela home" in resultado
    assert "- verificar contraste (WCAG 1.4.3)" in resultado
    assert (
        "- **Visibilidade do status do sistema** — o fluxo não informa o usuário após cada etapa"
        in resultado
    )
    assert "Fora de escopo desta fase" in resultado
    assert "Não gerado por este agente" in resultado
    assert "revisar as recomendações de acessibilidade (seção 6, 1 item(ns))" in resultado
    assert "observações de usabilidade (seção 10, 1 item(ns))" in resultado
    assert "| User Flow: Agendamento assistido | trecho 1 |" in resultado
    assert "| Information Architecture | trecho 2 |" in resultado
    assert "| PRD de origem | https://example.atlassian.net/wiki/pages/1179649/PRD |" in resultado
    assert "| Story/Epic de origem | AQUAQE-11 |" in resultado


def test_format_ux_specification_markdown_sem_separador_nao_negrita_topico():
    spec = UXSpecification(
        id="UX-002", title="t", context_problem="c", review_notes=["nota simples sem topico"]
    )

    resultado = format_ux_specification_markdown(spec)

    assert "- nota simples sem topico" in resultado
    assert "**nota simples" not in resultado


def test_format_ux_specification_markdown_avisa_ausencia_de_personas_e_journey():
    spec = UXSpecification(id="UX-003", title="t", context_problem="c")

    resultado = format_ux_specification_markdown(spec)

    assert "Não disponível no PRD de origem — nenhuma seção de Personas identificada." in resultado
    assert (
        "Não disponível no PRD de origem — nenhuma seção de User Journey identificada."
        in resultado
    )


def test_format_ux_specification_markdown_omits_empty_sections_gracefully():
    spec = UXSpecification(id="UX-004", title="t", context_problem="c")

    resultado = format_ux_specification_markdown(spec)

    assert "(nenhum)" in resultado
    assert "(nenhuma)" in resultado
    assert "**PRD de origem**: (não informado)" in resultado
    assert "**Story/Epic de origem**: (não informado)" in resultado
    assert "| PRD de origem | (não informado) |" in resultado
