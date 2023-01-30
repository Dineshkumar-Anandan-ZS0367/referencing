import pytest

from referencing import Resource, Specification
import referencing.jsonschema


@pytest.mark.parametrize(
    "uri, expected",
    [
        (
            "https://json-schema.org/draft/2020-12/schema",
            referencing.jsonschema.DRAFT202012,
        ),
        (
            "https://json-schema.org/draft/2019-09/schema",
            referencing.jsonschema.DRAFT201909,
        ),
        (
            "http://json-schema.org/draft-07/schema#",
            referencing.jsonschema.DRAFT7,
        ),
        (
            "http://json-schema.org/draft-06/schema#",
            referencing.jsonschema.DRAFT6,
        ),
        (
            "http://json-schema.org/draft-04/schema#",
            referencing.jsonschema.DRAFT4,
        ),
        (
            "http://json-schema.org/draft-03/schema#",
            referencing.jsonschema.DRAFT3,
        ),
    ],
)
def test_schemas_with_explicit_schema_keywords_are_detected(uri, expected):
    """
    The $schema keyword in JSON Schema is a dialect identifier.
    """
    contents = {"$schema": uri}
    resource = Resource.from_contents(contents)
    assert resource == Resource(contents=contents, specification=expected)


def test_unknown_dialect():
    dialect_id = "http://example.com/unknown-json-schema-dialect-id"
    with pytest.raises(referencing.jsonschema.UnknownDialect) as excinfo:
        Resource.from_contents({"$schema": dialect_id})
    assert excinfo.value.uri == dialect_id


@pytest.mark.parametrize(
    "id, specification",
    [
        ("$id", referencing.jsonschema.DRAFT202012),
        ("$id", referencing.jsonschema.DRAFT201909),
        ("$id", referencing.jsonschema.DRAFT7),
        ("$id", referencing.jsonschema.DRAFT6),
        ("id", referencing.jsonschema.DRAFT4),
        ("id", referencing.jsonschema.DRAFT3),
    ],
)
def test_id_of_mapping(id, specification):
    uri = "http://example.com/some-schema"
    assert specification.id_of({id: uri}) == uri


@pytest.mark.parametrize(
    "specification",
    [
        referencing.jsonschema.DRAFT202012,
        referencing.jsonschema.DRAFT201909,
        referencing.jsonschema.DRAFT7,
        referencing.jsonschema.DRAFT6,
    ],
)
@pytest.mark.parametrize("value", [True, False])
def test_id_of_bool(specification, value):
    assert specification.id_of(value) is None


@pytest.mark.parametrize(
    "specification",
    [
        referencing.jsonschema.DRAFT202012,
        referencing.jsonschema.DRAFT201909,
        referencing.jsonschema.DRAFT7,
        referencing.jsonschema.DRAFT6,
    ],
)
@pytest.mark.parametrize("value", [True, False])
def test_anchors_in_bool(specification, value):
    assert specification.anchors_in(value) == []


@pytest.mark.parametrize(
    "uri, expected",
    [
        (
            "https://json-schema.org/draft/2020-12/schema",
            referencing.jsonschema.DRAFT202012,
        ),
        (
            "https://json-schema.org/draft/2019-09/schema",
            referencing.jsonschema.DRAFT201909,
        ),
        (
            "http://json-schema.org/draft-07/schema#",
            referencing.jsonschema.DRAFT7,
        ),
        (
            "http://json-schema.org/draft-06/schema#",
            referencing.jsonschema.DRAFT6,
        ),
        (
            "http://json-schema.org/draft-04/schema#",
            referencing.jsonschema.DRAFT4,
        ),
        (
            "http://json-schema.org/draft-03/schema#",
            referencing.jsonschema.DRAFT3,
        ),
    ],
)
def test_specification_with(uri, expected):
    assert referencing.jsonschema.specification_with(uri) == expected


def test_specification_with_unknown_dialect():
    dialect_id = "http://example.com/unknown-json-schema-dialect-id"
    with pytest.raises(referencing.jsonschema.UnknownDialect) as excinfo:
        referencing.jsonschema.specification_with(dialect_id)
    assert excinfo.value.uri == dialect_id


def test_specification_with_default():
    dialect_id = "http://example.com/unknown-json-schema-dialect-id"
    specification = referencing.jsonschema.specification_with(
        dialect_id,
        default=Specification.OPAQUE,
    )
    assert specification is Specification.OPAQUE
