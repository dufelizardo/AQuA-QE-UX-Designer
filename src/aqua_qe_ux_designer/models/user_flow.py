from dataclasses import dataclass, field


@dataclass
class UserFlow:
    """Fluxo de navegação concreto para uma tarefa, conforme docs/agent/output_schema.md."""

    name: str
    steps: list[str] = field(default_factory=list)
    source_reference: str = ""
