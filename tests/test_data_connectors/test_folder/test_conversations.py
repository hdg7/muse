import os.path

from pytest import fixture

from muse.data_importer import import_data


@fixture
def folder_path():
    return os.path.join(os.path.dirname(__file__), "conversation")


def test_import_data_csv(folder_path):
    conversations = import_data(folder_path, "conversation")
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
