from dataclasses import dataclass, field

from .information_architecture import InformationArchitecture
from .status import ArtifactStatus
from .user_flow import UserFlow


@dataclass
class UXSpecification:
    """UX Specification (UXS), conforme docs/agent/output_schema.md."""

    id: str
    title: str
    context_problem: str
    user_flows: list[UserFlow] = field(default_factory=list)
    information_architecture: InformationArchitecture = field(
        default_factory=InformationArchitecture
    )
    accessibility_recommendations: list[str] = field(default_factory=list)
    source_reference: str = ""
    prd_reference: str = ""
    ticket_reference: str = ""
    personas_reference: str = ""
    journey_reference: str = ""
    status: ArtifactStatus = ArtifactStatus.PENDING_CLARIFICATION
    review_notes: list[str] = field(default_factory=list)
