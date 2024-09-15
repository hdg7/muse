from muse.data_fetcher.data_fetcher import DataFetcher, RawData, ResourceMetadata
from muse.utils.resource_errors import UnknownResourceError


def fetch_data(data_path: str) -> RawData:
    """
    Fetch raw data from a given path.

    :param data_path: Path to the data to be fetched.
    :return: Raw data.
    :raises NotImplementedError: If the method is not implemented in the subclass.
    :raises ResourceNotFoundError: If the resource is not found.
    """
    for fetcher in DataFetcher.__subclasses__():
        if fetcher().check_data_path(data_path):
            return fetcher().fetch_data(data_path)

    raise UnknownResourceError(data_path)
