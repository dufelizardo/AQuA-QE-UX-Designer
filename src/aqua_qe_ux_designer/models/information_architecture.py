from dataclasses import dataclass, field


@dataclass
class InformationArchitecture:
    """Mapa de navegação/categorização do Épico, conforme docs/agent/output_schema.md."""

    sections: list[str] = field(default_factory=list)
    navigation_notes: str = ""
    source_reference: str = ""
