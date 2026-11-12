from src.extraction.ontology import ENTITY_TYPES


def test_ontology_is_not_empty():

    assert len(ENTITY_TYPES) > 0


def test_core_entity_types_exist():

    required_types = {
        "PERSON",
        "EMAIL",
        "PHONE",
        "LOCATION",
        "COMPANY",
        "JOB_TITLE",
        "SKILL",
        "TECHNOLOGY",
        "DEGREE",
        "INSTITUTION",
        "PROJECT",
        "CERTIFICATION",
    }

    for entity_type in required_types:

        assert entity_type in ENTITY_TYPES


def test_ontology_contains_resume_information_types():

    expected_types = {
        "RESPONSIBILITY",
        "ACHIEVEMENT",
        "DATE",
        "DURATION",
        "INDUSTRY",
        "DOMAIN",
        "LANGUAGE",
    }

    for entity_type in expected_types:

        assert entity_type in ENTITY_TYPES


def test_ontology_types_are_strings():

    for entity_type in ENTITY_TYPES:

        assert isinstance(entity_type, str)
        assert entity_type.strip() != ""