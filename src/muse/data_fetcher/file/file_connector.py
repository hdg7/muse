import os

from ...utils import ResourceNotFoundError
from ..data_fetcher import DataFetcher, RawData


class FileConnector(DataFetcher):
    """
    Class for fetching data from files.
    """

    def fetch_data(self, data_path: str) -> RawData:
        if not self.check_data_path(data_path):
            raise ResourceNotFoundError(data_path)

        with open(data_path, "r") as file:
            return RawData(
                file.read(),
                metadata={"path": data_path, "file_type": data_path.rsplit(".", 1)[1]},
            )

    def check_data_path(self, data_path: str) -> bool:
        return os.path.isfile(data_path)
