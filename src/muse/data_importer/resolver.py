from typing import Union

from muse.data_fetcher.data_fetcher import RawData
from muse.data_importer.data_importer import Importer
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.utils.resource_errors import UnknownResourceError


def import_data(
    data_path: str,
    document_type: str,
    options: dict[str, any] = None
) -> Union[list[Document], list[MultiDocument]]:
    """
    Import raw data from a given path.

    :param data_path: Path to the data to be imported.
    :param document_type: Type of document to import, either 'document' or 'multi-document'.
    :param options: Options to initialize the data importer.
    :return: Raw data.
    """
    for importer in Importer.__subclasses__():
        importer = importer(options)
        if importer.check_data(data_path, document_type):
            return importer.import_data(data_path, document_type)

    raise UnknownResourceError(data_path)
