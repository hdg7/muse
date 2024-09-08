from abc import ABC, abstractmethod
from typing import Union

from ..data_manager import MultiDocument, Document
from ..data_fetcher.dataFetcher import RawData


class Importer(ABC):
    """
    Abstract class for importing data from different sources.

    It has two abstract methods:
    - import_data: Import data from a given path by resolving the kind of data it is and returning the
                   appropriate object.
    - check_data_path: Check if the data path belongs to this connector.
    """
    @abstractmethod
    def import_data(self, data: RawData, document_type: str) -> Union[Document, MultiDocument]:
        """
        Import data from a given path by resolving the kind of data it is and returning the appropriate object.

        :param data: The raw data to be imported.
        :param document_type: Type of document to import, either 'document', 'multi-document', or 'conversation'.
        :return: Document, MultiDocument, or Conversation object.
        :raises ValueError: If the document type is not 'document', 'multi-document', or 'conversation'.
        :raises InvalidResourceError: If the resource is invalid.
        :raises NotImplementedError: If the method is not implemented in the subclass, or the document type
                                     is not implemented for the resource.
        """
        pass

    @abstractmethod
    def check_data(self, data: RawData, document_type: str) -> bool:
        """
        Check if the data belongs to this connector.

        :param data: The raw data to be checked.
        :param document_type: Type of document to check, either 'document' or 'multi-document', or 'conversation'.
        :return: True if the data path belongs to this connector, False otherwise.
        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        pass
