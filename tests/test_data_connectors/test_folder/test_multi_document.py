import os.path

from pytest import fixture

from muse.data_importer import import_data


@fixture
def folder_path():
    return os.path.join(os.path.dirname(__file__), "multidoc")


def test_import_data_csv(folder_path):
    multidocs = import_data(folder_path, "multi-document")
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
