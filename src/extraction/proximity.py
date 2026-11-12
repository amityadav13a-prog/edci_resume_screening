def vertical_distance(entity_a, entity_b):

    if entity_a.page != entity_b.page:
        return float("inf")

    y_a = entity_a.metadata.get(
        "y0"
    )

    y_b = entity_b.metadata.get(
        "y0"
    )

    if y_a is None or y_b is None:
        return float("inf")

    return abs(
        y_a - y_b
    )
"""
FILE PURPOSE:
Provides layout-based proximity information between text/entities.

It measures how physically close entities are on a document page.
This can provide supporting evidence when identifying relationships.

LIMITATION:
Physical proximity does not guarantee semantic relationships,
especially in multi-column resumes, so it must be combined with
textual and contextual signals.
"""