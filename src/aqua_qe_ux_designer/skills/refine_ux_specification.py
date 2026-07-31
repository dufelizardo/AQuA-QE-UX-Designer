from ..models import InformationArchitecture, UserFlow, UXSpecification
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você refina uma UX Specification existente com base nas respostas que quem a propôs deu "
    "às perguntas de esclarecimento levantadas por um revisor. Baseie-se apenas na UX "
    "Specification atual e nas respostas fornecidas; nunca invente um fluxo, seção de "
    "arquitetura da informação ou recomendação de acessibilidade que não tenha sido "
    "informado neles — e nunca gere uma Persona ou User Journey nova (GR-UX-4). Nunca "
    "remova ou resuma um detalhe que já existe em um campo atual, a menos que uma resposta "
    "contradiga esse detalhe especificamente — preserve o texto existente nos campos que as "
    "respostas não abordam. Responda sempre em português."
)


def refine_ux_specification(spec: UXSpecification, respostas: list[dict]) -> UXSpecification:
    """Reescreve os campos da UX Specification usando as respostas do usuário, preservando o que as respostas não abordam."""
    fluxos_atuais = [{"nome": f.name, "passos": f.steps} for f in spec.user_flows]
    perguntas_respostas = [f"P: {item['pergunta']}\nR: {item['resposta']}" for item in respostas]

    prompt = (
        f"Título atual: {spec.title}\n"
        f"Contexto atual: {spec.context_problem}\n"
        f"Fluxos atuais: {fluxos_atuais}\n"
        f"Seções de IA atuais: {spec.information_architecture.sections}\n"
        f"Notas de navegação atuais: {spec.information_architecture.navigation_notes}\n"
        f"Recomendações de acessibilidade atuais: {spec.accessibility_recommendations}\n\n"
        "Respostas às perguntas de esclarecimento:\n"
        + "\n".join(perguntas_respostas)
        + "\n\nReescreva os campos incorporando essas respostas, resolvendo as lacunas "
        "apontadas. Campos (ou itens de lista) que não têm relação com nenhuma das "
        "respostas acima devem manter o texto atual, com o mesmo nível de detalhe — nunca "
        "simplifique um item para menos palavras do que já tinha.\n\n"
        'Responda apenas em JSON: {"titulo": "...", "contexto": "...", '
        '"fluxos": [{"nome": "...", "passos": ["..."]}], "secoes_ia": ["..."], '
        '"notas_navegacao": "...", "acessibilidade": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)

    spec.title = dados.get("titulo") or spec.title
    spec.context_problem = dados.get("contexto") or spec.context_problem
    spec.accessibility_recommendations = (
        dados.get("acessibilidade") or spec.accessibility_recommendations
    )

    novos_fluxos = [
        UserFlow(
            name=item.get("nome", ""),
            steps=item.get("passos", []),
            source_reference=spec.source_reference,
        )
        for item in dados.get("fluxos", [])
    ]
    spec.user_flows = novos_fluxos or spec.user_flows

    novas_secoes = dados.get("secoes_ia")
    novas_notas = dados.get("notas_navegacao")
    if novas_secoes or novas_notas:
        spec.information_architecture = InformationArchitecture(
            sections=novas_secoes or spec.information_architecture.sections,
            navigation_notes=novas_notas or spec.information_architecture.navigation_notes,
            source_reference=spec.information_architecture.source_reference,
        )

    return spec
