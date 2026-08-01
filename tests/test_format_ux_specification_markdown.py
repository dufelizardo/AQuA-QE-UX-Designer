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
        recommendations_synthesis=["priorizar feedback visual após cada etapa do agendamento"],
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
    assert "Seções:\n\n- Início\n- Agendamentos" in resultado
    assert "Agendamentos acessível pela home" in resultado
    assert "- verificar contraste (WCAG 1.4.3)" in resultado
    assert (
        "- **Visibilidade do status do sistema** — o fluxo não informa o usuário após cada etapa"
        in resultado
    )
    assert "Fora de escopo desta fase" in resultado
    assert "Não gerado por este agente" in resultado
    assert "devem ser extraídas literalmente do PRD de origem" in resultado
    assert "deve ser extraída literalmente do PRD de origem" in resultado
    assert "- priorizar feedback visual após cada etapa do agendamento" in resultado
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


def test_format_ux_specification_markdown_negrita_topico_com_dois_pontos():
    """Regressão (achado ao vivo): o phi4 às vezes devolve a observação já formatada com
    ': ' (dois pontos) em vez de ' — ' (travessão) — o destaque em negrito precisa cobrir
    os dois casos."""
    spec = UXSpecification(
        id="UX-005",
        title="t",
        context_problem="c",
        review_notes=[
            "Consistência e padrões: o fluxo pode quebrar a consistência com outros serviços"
        ],
    )

    resultado = format_ux_specification_markdown(spec)

    assert (
        "- **Consistência e padrões**: o fluxo pode quebrar a consistência com outros serviços"
        in resultado
    )


def test_format_ux_specification_markdown_negrita_topico_de_ate_dez_palavras():
    """Regressão (achado ao vivo): um tópico heurístico legítimo de 8 palavras
    ("Flexibilidade e eficiência do caminho para o uso") não estava sendo negritado
    porque a guarda antiga (6 palavras) era curta demais."""
    nota = (
        "Flexibilidade e eficiência do caminho para o uso: o processo pode exigir "
        "navegação física entre seções"
    )
    spec = UXSpecification(id="UX-007", title="t", context_problem="c", review_notes=[nota])

    resultado = format_ux_specification_markdown(spec)

    assert "- **Flexibilidade e eficiência do caminho para o uso**:" in resultado


def test_format_ux_specification_markdown_nao_negrita_frase_longa_com_dois_pontos():
    """Uma frase comum com ':' no meio (não um tópico curto) não deve virar negrito por engano."""
    nota = (
        "O fluxo de navegação sugere que o usuário deve ser redirecionado para um cadastro: "
        "isso pode quebrar a consistência com os demais serviços do site"
    )
    spec = UXSpecification(id="UX-006", title="t", context_problem="c", review_notes=[nota])

    resultado = format_ux_specification_markdown(spec)

    assert f"- {nota}" in resultado
    assert "**O fluxo" not in resultado


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


def test_format_ux_specification_markdown_rastreabilidade_achata_trecho_multilinha():
    """Regressão (achado ao vivo, Groq): identify_user_flows às vezes devolve o PRD inteiro
    (com múltiplas linhas) como trecho_fonte, o que quebrava a sintaxe de tabela Markdown
    (uma linha de tabela precisa ficar numa única linha)."""
    trecho_multilinha = "Linha um do PRD.\nLinha dois do PRD.\nLinha três do PRD."
    spec = UXSpecification(
        id="UX-008",
        title="t",
        context_problem="c",
        user_flows=[UserFlow(name="Fluxo", steps=["a", "b"], source_reference=trecho_multilinha)],
    )

    resultado = format_ux_specification_markdown(spec)

    assert "| User Flow: Fluxo | Linha um do PRD. Linha dois do PRD. Linha três do PRD. |" in resultado
    assert "\n| User Flow" in resultado
    linha_tabela = next(
        linha for linha in resultado.splitlines() if linha.startswith("| User Flow: Fluxo")
    )
    assert "\n" not in linha_tabela


def test_format_ux_specification_markdown_rastreabilidade_trunca_trecho_longo():
    trecho_longo = "x" * 500
    spec = UXSpecification(
        id="UX-009",
        title="t",
        context_problem="c",
        user_flows=[UserFlow(name="Fluxo", steps=["a", "b"], source_reference=trecho_longo)],
    )

    resultado = format_ux_specification_markdown(spec)

    assert f"| User Flow: Fluxo | {'x' * 200}… |" in resultado
