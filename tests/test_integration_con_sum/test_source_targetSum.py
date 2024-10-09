import os

from pytest import fixture

from muse.data_importer import import_data
from muse.summarizer import Sumy


@fixture
def document_path():
    return os.path.join(os.path.dirname(__file__), "doc")


def test_import_document_source_target(document_path):
    documents = import_data(document_path, "document", "en")
    assert isinstance(documents, list)
    assert len(documents) == 5

    sumy = Sumy({})
    for doc in documents:
        if doc.metadata["resource_name"].endswith("-0"):
            assert doc.text.startswith(
                "The Met Office has issued a yellow weather warning for"
            )
            assert doc.summary.startswith(
                "Winds could reach gale force in Wales with stormy"
            )
    summary = sumy.summarize(documents)
    assert len(summary) == len(documents)
    print(summary[1])
    print(documents[1].summary)
