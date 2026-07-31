from ..models import ArtifactStatus, UXSpecification
from ..skills.design_information_architecture import design_information_architecture
from ..skills.extract_ux_context import extract_ux_context
from ..skills.identify_user_flows import identify_user_flows
from ..skills.refine_ux_specification import refine_ux_specification as _refinar_campos
from ..skills.review_accessibility import review_accessibility
from ..skills.review_ux_specification import review_ux_specification
from ..skills.validate_ux_specification import validate_ux_specification


def finalize_ux_specification(spec: UXSpecification) -> UXSpecification:
    """Aplica o checklist automático e a revisão por LLM, decidindo o status final da UX Specification."""
    motivos_checklist = validate_ux_specification(spec)
    if motivos_checklist:
        spec.status = ArtifactStatus.PENDING_CLARIFICATION
        spec.review_notes = motivos_checklist
        return spec

    revisao = review_ux_specification(spec)
    spec.review_notes = revisao["problemas"]
    spec.status = (
        ArtifactStatus.DRAFT_VALIDATED
        if revisao["aprovado"]
        else ArtifactStatus.PENDING_CLARIFICATION
    )
    return spec


def refine_and_finalize_ux_specification(
    spec: UXSpecification, respostas: list[dict]
) -> UXSpecification:
    """Reescreve a UX Specification com as respostas do usuário e reaplica validate/review, atualizando status e review_notes."""
    spec_refinada = _refinar_campos(spec, respostas)
    return finalize_ux_specification(spec_refinada)


def generate_ux_specification(
    texto_prd: str,
    texto_ticket: str,
    prd_reference: str = "",
    ticket_reference: str = "",
) -> UXSpecification:
    """Gera a UX Specification a partir do PRD e da Story/Epic de origem, orquestrando a sequência padrão de skills.

    `prd_reference`/`ticket_reference` são a URL/ID do Confluence e a chave do Jira informados
    pelo usuário (não o texto lido) — usados apenas para a seção 2 (Escopo) do export em
    Markdown, nunca para leitura.
    """
    contexto = extract_ux_context(texto_prd, texto_ticket)
    fluxo = identify_user_flows(texto_ticket, contexto)
    arquitetura_informacao = design_information_architecture(texto_ticket, contexto)
    recomendacoes_acessibilidade = review_accessibility(fluxo, arquitetura_informacao)

    fonte = f"PRD:\n{texto_prd}\n\nStory/Epic:\n{texto_ticket}"
    spec = UXSpecification(
        id="UX-001",
        title=contexto["title"],
        context_problem=contexto["context_problem"],
        user_flows=[fluxo],
        information_architecture=arquitetura_informacao,
        accessibility_recommendations=recomendacoes_acessibilidade,
        source_reference=fonte,
        prd_reference=prd_reference,
        ticket_reference=ticket_reference,
        personas_reference=contexto.get("personas_reference", ""),
        journey_reference=contexto.get("journey_reference", ""),
    )
    return finalize_ux_specification(spec)
