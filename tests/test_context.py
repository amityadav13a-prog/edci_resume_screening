from src.extraction.context import get_context


def test_context_contains_entity():

    text = (
        "Rahul Sharma worked at Amazon "
        "as a Software Engineer from 2021 to 2024."
    )

    start = text.index("Amazon")
    end = start + len("Amazon")

    context = get_context(
        text,
        start,
        end,
    )

    assert "Amazon" in context


def test_context_returns_surrounding_text():

    text = (
        "Rahul Sharma worked at Amazon "
        "as a Software Engineer from 2021 to 2024."
    )

    start = text.index("Amazon")
    end = start + len("Amazon")

    context = get_context(
        text,
        start,
        end,
        window=30,
    )

    assert "worked at" in context
    assert "Software Engineer" in context


def test_context_does_not_exceed_text():

    text = "Python AWS Docker"

    start = text.index("Python")
    end = start + len("Python")

    context = get_context(
        text,
        start,
        end,
        window=1000,
    )

    assert context == text