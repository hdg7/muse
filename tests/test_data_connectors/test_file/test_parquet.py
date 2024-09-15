import os.path

from pytest import fixture

from muse.data_fetcher import fetch_data
from muse.data_importer import import_data


@fixture
def parquet_path():
    return os.path.join(os.path.dirname(__file__), "test.parquet")


def test_fetch_data_parquet(parquet_path):
    data = fetch_data(parquet_path)
    assert data["metadata"]["resource_name"] == parquet_path
    assert data["metadata"]["resource_type"] == "parquet"
    assert data["metadata"]["data_kind"] is None


def test_import_data_csv(parquet_path):
    data = fetch_data(parquet_path)
    documents = import_data(data, "document")
    assert isinstance(documents, list)
    assert len(documents) == 10
    assert documents[0].text.startswith(
        "the interest in anchoring phenomena and phenomena in confined nematic liquid crystals has largely been driven by their potential use in liquid crystal display devices"
    )
    assert documents[0].summary.startswith(
        "we study the phase behavior of a nematic liquid crystal confined between a flat substrate with strong anchoring and a patterned substrate whose structure and local anchoring strength we vary ."
    )
