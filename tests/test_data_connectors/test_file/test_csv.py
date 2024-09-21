import os.path

from pytest import fixture

from muse.data_fetcher import fetch_data
from muse.data_importer import import_data


@fixture
def csv_path():
    return os.path.join(os.path.dirname(__file__), "test.csv")


def test_import_data_csv(csv_path):
    documents = import_data(csv_path, "document")
    assert isinstance(documents, list)
    assert len(documents) == 4
    assert documents[-1].metadata["date"] == "2022-07-01 08:29:01"
