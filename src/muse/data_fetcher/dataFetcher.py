from abc import ABC, abstractmethod


class RawData:
    """
    Class for raw data.
    """

    def __init__(self, data: str, metadata: dict | None = None):
        """
        Initialize the raw data.

        :param data: Raw data.
        :param metadata: Metadata of the raw data.
        """
        self.data = data
        self.metadata = metadata


class DataFetcher(ABC):
    """
    Abstract class for fetching data from different sources.

    It has two abstract methods:
    - fetch_data: Fetch raw data from a given path.
    - check_data_path: Check if the data path belongs to this connector.
    """

    @abstractmethod
    def fetch_data(self, data_path: str) -> RawData:
        """
        Fetch raw data from a given path.

        :param data_path: Path to the data to be fetched.
        :return: Raw data.
        :raises NotImplementedError: If the method is not implemented in the subclass.
        :raises ResourceNotFoundError: If the resource is not found.
        """
        pass

    @abstractmethod
    def check_data_path(self, data_path: str) -> bool:
        """
        Check if the data path belongs to this connector.

        :param data_path: Path to the data to be checked.
        :return: True if the data path belongs to this connector, False otherwise.
        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        pass
