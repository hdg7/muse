from abc import ABC, abstractmethod
from typing import Union

from .. import MultiDocument, Document


class Importer(ABC):
    """
    Abstract class for importing data from different sources.

    It has two abstract methods:
    - import_data: Import data from a given path by resolving the kind of data it is and returning the
                   appropriate object.
    - check_data_path: Check if the data path belongs to this connector.
    """
    @abstractmethod
    def import_data(self, data_path: str, document_type: str) -> Union[Document, MultiDocument]:
        """
        Import data from a given path by resolving the kind of data it is and returning the appropriate object.

        :param data_path: Path to the data to be imported.
        :param document_type: Type of document to import, either 'document' or 'multi-document'.
        :return: Document or MultiDocument object.
        :raises ValueError: If the document type is not 'document' or 'multi-document'.
        :raises UnknownResourceError: If the resource is not recognized.
        :raises ResourceNotFoundError: If the resource is not found.
        :raises InvalidResourceError: If the resource is invalid.
        """
        pass

    @abstractmethod
    def check_data_path(self, data_path: str) -> bool:
        """
        Check if the data path belongs to this connector.

        :param data_path: Path to the data to be imported.
        :return: True if the data path belongs to this connector, False otherwise.
        :raises NotImplementedError: If the method is not implemented in the subclass.
        """
        pass


def import_data(self, data_path: str, document_type: str) -> Union[Document, MultiDocument]:
    """
    Import data from a given path by resolving the kind of data it is and returning the appropriate object.

    :param self:
    :param data_path: Path to the data to be imported.
    :param document_type: Type of document to import, either 'document' or 'multi-document'.
    :return: Document or MultiDocument object.
    :raises NotImplementedError: If the method is not implemented in the subclass.
    :raises ValueError: If the document type is not 'document' or 'multi-document'.
    :raises UnknownResourceError: If the resource is not recognized.
    :raises ResourceNotFoundError: If the resource is not found.
    :raises InvalidResourceError: If the resource is invalid.
    """
    pass
