from abc import ABC, abstractmethod
from typing import TypedDict


class ResourceMetadata(TypedDict):
    """
    Type definition for resource metadata.
    """

    resource_name: str
    resource_type: str
    data_kind: str | None


class RawData(TypedDict):
    """
    Type definition for raw data.
    """

    data: str | bytes | list["RawData"]
    metadata: ResourceMetadata


class DataFetcher(ABC):
    """
    Abstract class for fetching data from different sources.

    It has two abstract methods:
    - fetch_data: Fetch raw data from a given path.
    - check_data_path: Check if the data path belongs to this connector.
    """
    @abstractmethod
    def __init__(self, options: dict[str, any]):
        """
        Initialize the data fetcher.

        :param options: Options to initialize the data fetcher.
        """
        pass

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
