import os.path

from pytest import fixture

from muse.data_importer import import_data


@fixture
def document_path():
    return os.path.join(os.path.dirname(__file__), "doc")


@fixture
def multi_document_path():
    return os.path.join(os.path.dirname(__file__), "multidoc")


@fixture
def conversations_path():
    return os.path.join(os.path.dirname(__file__), "conversation")


def test_import_document_folder(document_path):
    documents = import_data(document_path, "document", "en")
    assert isinstance(documents, list)
    assert len(documents) == 2
    for document in documents:
        if document.metadata["resource_name"] == "foo.txt":
            assert document.text.startswith("Urban green spaces,")
            assert document.summary.startswith(
                "Urban green spaces provide environmental"
            )
        elif document.metadata["resource_name"] == "bar.txt":
            assert document.text.startswith("Electric vehicles (EVs) are transforming")
            assert document.summary.startswith(
                "Electric vehicles (EVs) are gaining traction "
            )


def test_import_multi_document_folder(multi_document_path):
    multidocs = import_data(multi_document_path, "multi-document", "en")
    assert isinstance(multidocs, list)
    assert len(multidocs) == 2
    for multidoc in multidocs:
        if multidoc.metadata["resource_name"] == "foo":
            assert str(multidoc).startswith("Urban green spaces,")
            assert multidoc.summary.startswith(
                "Urban green spaces provide environmental"
            )
        elif multidoc.metadata["resource_name"] == "bar":
            assert "alternative to traditional internal combustion engine (ICE)" in str(
                multidoc
            )
            assert "Electric vehicles (EVs) are transforming" in str(multidoc)
            assert multidoc.summary.startswith(
                "Electric vehicles (EVs) are gaining traction "
            )


def test_import_conversations_folder(conversations_path):
    conversations = import_data(conversations_path, "conversation", "en")
    assert isinstance(conversations, list)
    assert len(conversations) == 2
    for conversation in conversations:
        if conversation.metadata["resource_name"] == "foo":
            assert str(conversation).startswith("Person1: To start this meeting,")
            assert conversation.summary.startswith("Three people discuss EVs")
        elif conversation.metadata["resource_name"] == "bar":
            assert str(conversation).startswith(
                "Person1: What are your plans for this weekend?"
            )
            assert conversation.summary.startswith(
                "Person1 and Person2 are discussing weekend plans"
            )
