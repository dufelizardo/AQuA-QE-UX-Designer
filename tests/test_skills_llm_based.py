from aqua_qe_ux_designer.models import InformationArchitecture, UserFlow, UXSpecification
from aqua_qe_ux_designer.skills import extract_ux_context as extract_ux_context_module
from aqua_qe_ux_designer.skills import (
    design_information_architecture as design_information_architecture_module,
)
from aqua_qe_ux_designer.skills import (
    generate_ux_clarifying_questions as generate_ux_clarifying_questions_module,
)
from aqua_qe_ux_designer.skills import identify_user_flows as identify_user_flows_module
from aqua_qe_ux_designer.skills import refine_ux_specification as refine_ux_specification_module
from aqua_qe_ux_designer.skills import review_accessibility as review_accessibility_module
from aqua_qe_ux_designer.skills import review_ux_specification as review_ux_specification_module


def _spec(**overrides) -> UXSpecification:
    base = {
        "id": "UX-001",
        "title": "titulo",
        "context_problem": "contexto",
        "source_reference": "fonte",
    }
    base.update(overrides)
    return UXSpecification(**base)


def test_extract_ux_context_maps_json_to_fields(monkeypatch):
    monkeypatch.setattr(
        extract_ux_context_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "titulo": "Agendamento de Consulta",
            "contexto": "contexto extraido",
            "personas_journeys": "Persona: Paciente idoso",
        },
    )

    contexto = extract_ux_context_module.extract_ux_context("prd", "story")

    assert contexto["title"] == "Agendamento de Consulta"
    assert contexto["context_problem"] == "contexto extraido"
    assert contexto["personas_journeys"] == "Persona: Paciente idoso"


def test_identify_user_flows_maps_json_to_userflow(monkeypatch):
    monkeypatch.setattr(
        identify_user_flows_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "nome": "Agendamento assistido",
            "passos": ["abrir tela", "escolher horário", "confirmar"],
            "trecho_fonte": "trecho 1",
        },
    )

    fluxo = identify_user_flows_module.identify_user_flows("story", {"context_problem": "c"})

    assert fluxo.name == "Agendamento assistido"
    assert fluxo.steps == ["abrir tela", "escolher horário", "confirmar"]
    assert fluxo.source_reference == "trecho 1"


def test_identify_user_flows_defaults_to_empty_steps(monkeypatch):
    monkeypatch.setattr(
        identify_user_flows_module, "complete_json", lambda prompt, system="", model=None: {}
    )

    fluxo = identify_user_flows_module.identify_user_flows("story", {})

    assert fluxo.name == ""
    assert fluxo.steps == []


def test_identify_user_flows_converte_passo_objeto_em_string(monkeypatch):
    """Regressão (achado ao vivo): o Ollama (mistral) às vezes devolve cada passo como
    {"passo": ..., "trecho_fonte": ...} em vez de uma string simples."""
    monkeypatch.setattr(
        identify_user_flows_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "nome": "Agendamento",
            "passos": [
                {"trecho_fonte": "trecho x", "passo": "abrir tela de agendamento"},
                {"trecho_fonte": "trecho y", "passo": "confirmar horário"},
            ],
            "trecho_fonte": "trecho 1",
        },
    )

    fluxo = identify_user_flows_module.identify_user_flows("story", {})

    assert fluxo.steps == ["abrir tela de agendamento", "confirmar horário"]


def test_design_information_architecture_maps_json_to_model(monkeypatch):
    monkeypatch.setattr(
        design_information_architecture_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "secoes": ["Início", "Agendamentos"],
            "notas_navegacao": "Agendamentos acessível pela home",
            "trecho_fonte": "trecho 1",
        },
    )

    ia = design_information_architecture_module.design_information_architecture(
        "epic", {"context_problem": "c"}
    )

    assert ia.sections == ["Início", "Agendamentos"]
    assert ia.navigation_notes == "Agendamentos acessível pela home"
    assert ia.source_reference == "trecho 1"


def test_design_information_architecture_converte_secao_objeto_em_string(monkeypatch):
    """Regressão (achado ao vivo): o Ollama (mistral) às vezes devolve cada seção como
    {"nome": ..., "descricao": ...} em vez de uma string simples."""
    monkeypatch.setattr(
        design_information_architecture_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "secoes": [
                {
                    "nome": "Agendamento Assistido",
                    "descricao": "Funcionalidade para quem não usa o app",
                    "subsecoes": [{"nome": "Regras de Negócio"}],
                }
            ],
            "notas_navegacao": "n",
            "trecho_fonte": "f",
        },
    )

    ia = design_information_architecture_module.design_information_architecture("epic", {})

    assert ia.sections == ["Agendamento Assistido: Funcionalidade para quem não usa o app"]


def test_review_accessibility_maps_json_to_list(monkeypatch):
    monkeypatch.setattr(
        review_accessibility_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "recomendacoes": ["verificar contraste (WCAG 1.4.3)"]
        },
    )

    fluxo = UserFlow(name="f", steps=["a", "b"], source_reference="x")
    ia = InformationArchitecture(sections=["Home"])

    resultado = review_accessibility_module.review_accessibility(fluxo, ia)

    assert resultado == ["verificar contraste (WCAG 1.4.3)"]


def test_review_accessibility_converte_recomendacao_objeto_em_string(monkeypatch):
    """Regressão (achado ao vivo): o Ollama (mistral) às vezes devolve cada recomendação como
    {"passo": ..., "criterio_wcag": ..., "acao": ...} em vez de uma string simples."""
    monkeypatch.setattr(
        review_accessibility_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "recomendacoes": [
                {
                    "passo": "O cliente confirma o agendamento",
                    "criterio_wcag": "2.4.3 Ordem de Foco",
                    "acao": "verificar se a ordem de tabulação segue a sequência lógica",
                }
            ]
        },
    )

    fluxo = UserFlow(name="f", steps=["a", "b"], source_reference="x")
    ia = InformationArchitecture(sections=["Home"])

    resultado = review_accessibility_module.review_accessibility(fluxo, ia)

    assert resultado == [
        "2.4.3 Ordem de Foco: verificar se a ordem de tabulação segue a sequência lógica"
    ]


def test_review_ux_specification_uses_review_model_and_maps_result(monkeypatch):
    captured = {}

    def fake_complete_json(prompt, system="", model=None):
        captured["model"] = model
        return {"aprovado": True, "problemas": []}

    monkeypatch.setattr(review_ux_specification_module, "complete_json", fake_complete_json)

    resultado = review_ux_specification_module.review_ux_specification(_spec())

    assert resultado == {"aprovado": True, "problemas": []}
    assert captured["model"] == "phi4"


def test_generate_ux_clarifying_questions_returns_empty_without_review_notes():
    assert (
        generate_ux_clarifying_questions_module.generate_ux_clarifying_questions(_spec()) == []
    )


def test_generate_ux_clarifying_questions_maps_json_to_list(monkeypatch):
    monkeypatch.setattr(
        generate_ux_clarifying_questions_module,
        "complete_json",
        lambda prompt, system="", model=None: {"perguntas": ["Qual o público-alvo principal?"]},
    )

    spec = _spec(review_notes=["fluxo sem confirmação visual"])
    perguntas = generate_ux_clarifying_questions_module.generate_ux_clarifying_questions(spec)

    assert perguntas == ["Qual o público-alvo principal?"]


def test_refine_ux_specification_rewrites_fields_from_answers(monkeypatch):
    monkeypatch.setattr(
        refine_ux_specification_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "titulo": "titulo refinado",
            "contexto": "contexto",
            "fluxos": [{"nome": "Agendamento", "passos": ["passo 1", "passo 2"]}],
            "secoes_ia": ["Início"],
            "notas_navegacao": "nota",
            "acessibilidade": ["verificar foco"],
        },
    )

    spec = _spec(title="titulo antigo")
    resultado = refine_ux_specification_module.refine_ux_specification(
        spec, [{"pergunta": "qual o titulo?", "resposta": "titulo refinado"}]
    )

    assert resultado.title == "titulo refinado"
    assert resultado.user_flows[0].name == "Agendamento"
    assert resultado.user_flows[0].steps == ["passo 1", "passo 2"]
    assert resultado.information_architecture.sections == ["Início"]
    assert resultado.accessibility_recommendations == ["verificar foco"]


def test_refine_ux_specification_preserva_campos_sem_resposta_relacionada(monkeypatch):
    """Sem fluxos/secoes_ia na resposta do LLM, mantém os valores atuais em vez de apagá-los."""
    monkeypatch.setattr(
        refine_ux_specification_module,
        "complete_json",
        lambda prompt, system="", model=None: {"titulo": "novo titulo"},
    )

    spec = _spec(
        title="titulo antigo",
        user_flows=[UserFlow(name="Agendamento", steps=["passo 1"], source_reference="f")],
        information_architecture=InformationArchitecture(sections=["Início"]),
    )

    resultado = refine_ux_specification_module.refine_ux_specification(spec, [])

    assert resultado.title == "novo titulo"
    assert resultado.user_flows[0].name == "Agendamento"
    assert resultado.information_architecture.sections == ["Início"]
