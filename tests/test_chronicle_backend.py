import pytest
from sigma.backends.chronicle import ChronicleBackend
from sigma.collection import SigmaCollection
from sigma.pipelines.chronicle import chronicle_windows_pipeline


@pytest.fixture
def chronicle_backend():
    return ChronicleBackend()


@pytest.fixture
def chronicle_custom_backend():
    return ChronicleBackend(
        query_settings=lambda x: {"custom.query.key": x.title},
        output_settings={"custom.key": "customvalue"},
    )


def test_chronicle_and_expression(chronicle_backend: ChronicleBackend):
    rule = SigmaCollection.from_yaml(
        """
            title: Test
            status: test
            logsource:
                category: test_category
                product: test_product
            detection:
                sel:
                    fieldA: valueA
                    fieldB: valueB
                condition: sel
        """
    )

    assert chronicle_backend.convert(rule) == ['fieldA="valueA" AND fieldB="valueB"']


def test_chronicle_or_expression(chronicle_backend: ChronicleBackend):
    rule = SigmaCollection.from_yaml(
        """
            title: Test
            status: test
            logsource:
                category: test_category
                product: test_product
            detection:
                sel1:
                    fieldA: valueA
                sel2:
                    fieldB: valueB
                condition: 1 of sel*
        """
    )
    assert chronicle_backend.convert(rule) == ['fieldA="valueA" OR fieldB="valueB"']


def test_chronicle_and_or_expression(chronicle_backend: ChronicleBackend):
    rule = SigmaCollection.from_yaml(
        """
            title: Test
            status: test
            logsource:
                category: test_category
                product: test_product
            detection:
                sel:
                    fieldA:
                        - valueA1
                        - valueA2
                    fieldB:
                        - valueB1
                        - valueB2
                condition: sel
        """
    )
    assert chronicle_backend.convert(rule) == [
        '((fieldA="valueA1" AND fieldB="valueB1") OR (fieldA="valueA1" AND fieldB="valueB2") OR (fieldA="valueA2" AND fieldB="valueB1") OR (fieldA="valueA2" AND fieldB="valueB2"))'
    ]


def test_chronicle_or_and_expression(chronicle_backend: ChronicleBackend):
    rule = SigmaCollection.from_yaml(
        """
            title: Test
            status: test
            logsource:
                category: test_category
                product: test_product
            detection:
                sel1:
                    fieldA: valueA1
                    fieldB: valueB1
                sel2:
                    fieldA: valueA2
                    fieldB: valueB2
                condition: 1 of sel*
        """
    )
    assert chronicle_backend.convert(rule) == [
        '(fieldA="valueA1" AND fieldB="valueB1") OR (fieldA="valueA2" AND fieldB="valueB2")'
    ]
