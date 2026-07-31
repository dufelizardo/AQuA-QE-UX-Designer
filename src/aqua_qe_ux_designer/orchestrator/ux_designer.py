from ..models import UXSpecification
from ..workflow.generate_ux_specification import generate_ux_specification


def handle_request(texto_prd: str, texto_ticket: str) -> UXSpecification:
    """Ponto de entrada único do agente — gera a UX Specification a partir do PRD e da Story/Epic de origem."""
    return generate_ux_specification(texto_prd, texto_ticket)
