import os.path

from pytest import fixture

from muse.data_importer import import_data


@fixture
def folder_path():
    return os.path.join(os.path.dirname(__file__), "doc")


def test_import_data_csv(folder_path):
    documents = import_data(folder_path, "document")
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
