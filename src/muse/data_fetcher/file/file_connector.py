import os

from muse.data_fetcher.data_fetcher import DataFetcher, RawData
from muse.utils.resource_errors import ResourceNotFoundError


class FileConnector(DataFetcher):
    """
    Class for fetching data from files.
    """

    def fetch_data(self, data_path: str) -> RawData:
        if not self.check_data_path(data_path):
            raise ResourceNotFoundError(data_path)

        text_extensions = ['txt', 'json', 'csv', 'html', 'xml', 'md', 'log']

        file_extension = data_path.rsplit(".", 1)[-1].lower()

        if file_extension in text_extensions:
            try:
                with open(data_path, "r") as file:
                    return {
                        "data": file.read(),
                        "metadata": {
                            "resource_name": data_path,
                            "resource_type": data_path.rsplit(".", 1)[1],
                            "data_kind": None,
                        },
                    }
            except UnicodeDecodeError:
                with open(data_path, "rb") as file:
                    return {
                        "data": file.read(),
                        "metadata": {
                            "resource_name": data_path,
                            "resource_type": data_path.rsplit(".", 1)[1],
                            "data_kind": None,
                        },
                    }
        else:
            with open(data_path, "rb") as file:
                return {
                    "data": file.read(),
                    "metadata": {
                        "resource_name": data_path,
                        "resource_type": data_path.rsplit(".", 1)[1],
                        "data_kind": None,
                    },
                }

    def check_data_path(self, data_path: str) -> bool:
        return os.path.isfile(data_path)
