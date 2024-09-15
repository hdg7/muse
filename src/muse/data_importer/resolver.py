from typing import Union

from muse.data_fetcher.data_fetcher import RawData
from muse.data_importer.data_importer import Importer
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.utils.resource_errors import UnknownResourceError


def import_data(
    data: RawData, document_type: str
) -> Union[list[Document], list[MultiDocument]]:
    """
    Import raw data from a given path.

    :param data: Raw data to be imported.
    :param document_type: Type of document to import, either 'document' or 'multi-document'.
    :return: Raw data.
    """
    for importer in Importer.__subclasses__():
        if importer().check_data(data, document_type):
            return importer().import_data(data, document_type)

    raise UnknownResourceError(data["metadata"]["resource_name"])
