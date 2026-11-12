def get_context(
    text: str,
    start: int,
    end: int,
    window: int = 80
) -> str:

    left = max(
        0,
        start - window
    )

    right = min(
        len(text),
        end + window
    )

    return text[left:right]

"""
FILE PURPOSE:
Extracts the surrounding text of a detected entity.

Context is used to provide additional information when determining
what an entity means.

Example:
"Amazon" becomes easier to classify when the surrounding text says
"worked at Amazon as a Software Engineer."

LIMITATION:
Character-based context is only a simple signal and can be affected
by unusual layouts such as multi-column resumes.
"""