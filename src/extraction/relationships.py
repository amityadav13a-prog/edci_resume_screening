from dataclasses import dataclass
from typing import Optional


@dataclass
class Relationship:

    relationship_type: str

    source_entity: str

    target_entity: str

    confidence: float

    evidence: Optional[str] = None

    """
FILE PURPOSE:
Identifies relationships between extracted entities.

Combines entity information, context, and document layout signals
to determine relationships such as:

Candidate -> EMPLOYED_AT -> Company
Employment -> HAS_JOB_TITLE -> Job Title
Project -> PROJECT_USES -> Technology

The resulting relationships are later used to build structured
student profiles.

LIMITATION:
The current implementation is mainly heuristic/rule-based and
can be improved with a trained relationship-extraction model.
"""