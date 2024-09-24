import os.path

from pytest import fixture

from muse.data_importer import import_data


@fixture
def document_csv_path():
    return os.path.join(os.path.dirname(__file__), "columnar_data", "doc.csv")


@fixture
def document_parquet_path():
    return os.path.join(os.path.dirname(__file__), "columnar_data", "doc.parquet")


@fixture
def multi_document_csv_path():
    return os.path.join(os.path.dirname(__file__), "columnar_data", "multi_doc.csv")


@fixture
def multi_document_parquet_path():
    return os.path.join(os.path.dirname(__file__), "columnar_data", "multi_doc.parquet")


@fixture
def conversation_csv_path():
    return os.path.join(os.path.dirname(__file__), "columnar_data", "conversation.csv")


@fixture
def conversation_parquet_path():
    return os.path.join(
        os.path.dirname(__file__), "columnar_data", "conversation.parquet"
    )


def test_import_document_csv(document_csv_path):
    documents = import_data(document_csv_path, "document", "en")
    assert isinstance(documents, list)
    assert len(documents) == 4
    assert documents[-1].metadata["date"] == "2022-07-01 08:29:01"


def test_import_document_parquet(document_parquet_path):
    documents = import_data(document_parquet_path, "document", "en")
    assert isinstance(documents, list)
    assert len(documents) == 10
    assert documents[0].text.startswith(
        "the interest in anchoring phenomena and phenomena in confined nematic liquid crystals has largely been driven by their potential use in liquid crystal display devices"
    )
    assert documents[0].summary.startswith(
        "we study the phase behavior of a nematic liquid crystal confined between a flat substrate with strong anchoring and a patterned substrate whose structure and local anchoring strength we vary ."
    )


def test_import_multi_doc_csv(multi_document_csv_path):
    documents = import_data(multi_document_csv_path, "multi-document", "en")
    assert isinstance(documents, list)
    assert len(documents) == 2


def test_import_multi_doc_parquet(multi_document_parquet_path):
    documents = import_data(multi_document_parquet_path, "multi-document", "en")
    assert isinstance(documents, list)
    assert len(documents) == 2


def test_import_parquet_conversation(conversation_parquet_path):
    documents = import_data(conversation_parquet_path, "conversation", "en")
    assert isinstance(documents, list)
    assert len(documents) == 9


def test_import_parquet_csv(conversation_csv_path):
    documents = import_data(conversation_csv_path, "conversation", "en")
    assert isinstance(documents, list)
    assert len(documents) == 9
