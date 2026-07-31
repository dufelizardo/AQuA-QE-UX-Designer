"""CLI simples para rodar o AQuA-QE UX Designer sem precisar mexer em sys.path manualmente."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

_RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(_RAIZ / "src"))
load_dotenv(_RAIZ / ".env")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from aqua_qe_ux_designer.models import ArtifactStatus, UXSpecification  # noqa: E402
from aqua_qe_ux_designer.orchestrator.ux_designer import handle_request  # noqa: E402
from aqua_qe_ux_designer.skills.create_confluence_page import create_confluence_page  # noqa: E402
from aqua_qe_ux_designer.skills.format_ux_specification_markdown import (  # noqa: E402
    format_ux_specification_markdown,
)
from aqua_qe_ux_designer.skills.generate_ux_clarifying_questions import (  # noqa: E402
    generate_ux_clarifying_questions,
)
from aqua_qe_ux_designer.skills.get_confluence_publish_location import (  # noqa: E402
    get_confluence_publish_location,
)
from aqua_qe_ux_designer.skills.read_confluence_page import read_confluence_page  # noqa: E402
from aqua_qe_ux_designer.skills.read_jira_issue import read_jira_issue  # noqa: E402
from aqua_qe_ux_designer.workflow.generate_ux_specification import (  # noqa: E402
    refine_and_finalize_ux_specification,
)


def _imprimir_spec(spec: UXSpecification) -> None:
    print(f"status: {spec.status.value}")
    print(f"título: {spec.title}")
    print(f"contexto: {spec.context_problem}")
    for fluxo in spec.user_flows:
        print(f"fluxo '{fluxo.name}': {len(fluxo.steps)} passo(s)")
    print(f"arquitetura da informação: {spec.information_architecture.sections}")
    print(f"recomendações de acessibilidade: {spec.accessibility_recommendations}")
    if spec.review_notes:
        print("observações da revisão:")
        for nota in spec.review_notes:
            print(f"  - {nota}")


def _perguntar_sim_nao(mensagem: str) -> bool:
    resposta = input(f"{mensagem} (s/n): ").strip().lower()
    return resposta in ("s", "sim", "y", "yes")


def _ciclo_de_refinamento(spec: UXSpecification) -> UXSpecification:
    """Gera perguntas, pede respostas ao usuário, refina e reavalia até aprovar ou o usuário desistir."""
    while spec.status != ArtifactStatus.DRAFT_VALIDATED and spec.review_notes:
        perguntas = generate_ux_clarifying_questions(spec)
        if not perguntas:
            break

        print("\nO revisor apontou problemas. Responda para ajudar a refinar a UX Specification:")
        respostas = []
        for pergunta in perguntas:
            resposta = input(f"  {pergunta}\n  > ")
            respostas.append({"pergunta": pergunta, "resposta": resposta})

        spec = refine_and_finalize_ux_specification(spec, respostas)
        print("\n--- UX Specification refinada ---")
        _imprimir_spec(spec)

        if spec.status != ArtifactStatus.DRAFT_VALIDATED and not _perguntar_sim_nao(
            "\nTentar refinar de novo?"
        ):
            break
    return spec


def _publicar_confluence(spec: UXSpecification, pagina_origem: str) -> None:
    """Publica a UX Specification como página nova no Confluence, irmã do PRD de origem, sempre sob confirmação humana explícita."""
    if not _perguntar_sim_nao("\nPublicar no Confluence como página irmã do PRD de origem?"):
        return
    titulo = input("Título da página no Confluence: ").strip()
    texto_formatado = format_ux_specification_markdown(spec)
    space_key, parent_page_id = get_confluence_publish_location(pagina_origem)
    url = create_confluence_page(texto_formatado, titulo, space_key, parent_page_id)
    print(f"publicado no Confluence: {url}")


def _rodar(
    texto_prd: str,
    texto_ticket: str,
    saida: str | None,
    refinar: bool,
    pagina_origem: str,
    publicar_confluence: bool,
) -> None:
    spec = handle_request(texto_prd, texto_ticket)
    _imprimir_spec(spec)

    if refinar:
        spec = _ciclo_de_refinamento(spec)

    if not _perguntar_sim_nao("\nAceitar esta UX Specification?"):
        return

    spec.status = ArtifactStatus.ACCEPTED

    if saida:
        with open(saida, "w", encoding="utf-8") as arquivo:
            arquivo.write(format_ux_specification_markdown(spec))
        print(f"exportado para: {saida}")

    if publicar_confluence:
        _publicar_confluence(spec, pagina_origem)


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o AQuA-QE UX Designer.")
    parser.add_argument(
        "--confluence",
        required=True,
        help="URL completa ou ID da página do Confluence Cloud com o PRD de origem.",
    )
    parser.add_argument(
        "--jira", required=True, help="Chave do ticket Jira da Story/Epic (ex.: AQUAQE-10)."
    )
    parser.add_argument("--saida", help="Caminho do .md exportado.")
    parser.add_argument(
        "--refinar",
        action="store_true",
        help=(
            "Ativa o ciclo interativo de perguntas/refinamento para a UX Specification não "
            "aprovada, antes do aceite humano (que é sempre perguntado, com ou sem esta flag)."
        ),
    )
    parser.add_argument(
        "--publicar-confluence",
        action="store_true",
        dest="publicar_confluence",
        help=(
            "Após aceitar a UX Specification, pergunta o título e publica como página nova "
            "no Confluence, irmã da página de origem do PRD."
        ),
    )
    args = parser.parse_args()

    texto_prd = read_confluence_page(args.confluence)
    texto_ticket = read_jira_issue(args.jira)
    _rodar(
        texto_prd,
        texto_ticket,
        args.saida,
        args.refinar,
        args.confluence,
        args.publicar_confluence,
    )


if __name__ == "__main__":
    main()
