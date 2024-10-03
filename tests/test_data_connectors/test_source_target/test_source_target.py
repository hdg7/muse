import os

from pytest import fixture

from muse.data_importer import import_data


@fixture
def document_path():
    return os.path.join(os.path.dirname(__file__), "doc")


def test_import_document_source_target(document_path):
    documents = import_data(document_path, "document", "en")
    assert isinstance(documents, list)
    assert len(documents) == 11536

    for doc in documents:
        if doc.metadata["resource_name"].endswith("-0"):
            assert doc.text.startswith(
                "A large void was temporarily plugged with granite"
            )
            assert doc.summary.startswith("Work to repair a sea wall")
