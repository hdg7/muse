import os.path

from pytest import fixture

from muse.data_fetcher import fetch_data
from muse.data_importer import import_data


@fixture
def folder_path():
    return os.path.join(os.path.dirname(__file__), "test")


def test_fetch_data_folder(folder_path):
    data = fetch_data(folder_path)
    assert data["metadata"]["resource_name"] == folder_path
    assert data["metadata"]["resource_type"] == "directory"
    assert data["metadata"]["data_kind"] is None


def test_import_data_csv(folder_path):
    data = fetch_data(folder_path)
    documents = import_data(data, "document")
    assert isinstance(documents, list)
    assert len(documents) == 2
    for document in documents:
        if document.metadata["resource_name"] == "foo.txt":
            assert document.text.startswith("Urban green spaces,")
            assert document.summary.startswith("Urban green spaces provide environmental")
        elif document.metadata["resource_name"] == "bar.txt":
            assert document.text.startswith("Electric vehicles (EVs) are transforming")
            assert document.summary.startswith("Electric vehicles (EVs) are gaining traction ")

