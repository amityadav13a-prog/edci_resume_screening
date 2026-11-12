from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Entity:

    text: str

    entity_type: str

    confidence: float

    page: Optional[int] = None

    source_text: Optional[str] = None

    normalized_value: Optional[str] = None

    start_char: Optional[int] = None

    end_char: Optional[int] = None

    metadata: dict = field(
        default_factory=dict
    )

    """
FILE PURPOSE:
Defines the Entity data structure used to represent information
extracted from resumes.

Each entity stores its text, semantic type, confidence, source/evidence,
location, and optional normalized value.

Example:
"Amazon" -> COMPANY

This structure is used by NER, deterministic extraction,
technology extraction, and later relationship/profile building.
"""