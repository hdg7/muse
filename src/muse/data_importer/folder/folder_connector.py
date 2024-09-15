from typing import Union

from muse.data_importer.data_importer import Importer
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.utils.resource_errors import InvalidResourceError


class FolderConnector(Importer):
    """
    Class for importing data from a folder.

    For Document:
        We expect to have a RawData object, with a data field consisting of one or two RawData objects, one for the text
        and one for the summary, if present.
    For MultiDocument:
        We expect to have a RawData object, with a data field consisting of a list of RawData objects, each of which
        contains a text and a summary, if present.
    For conversation (not yet implemented):
        We expect to have a RawData object, with a data field consisting of a list of RawData objects, each of which
        contains a conversation unit, we expect the temporal state to be in the metadata,
        encoded within the resource_name, along with any other relevant information, such as the speaker.
    """

    def __init__(self):
        self._invalid_reason = None

    def import_data(self, data, document_type):
        if not self.check_data(data, document_type):
            raise InvalidResourceError("Invalid data", self._invalid_reason)

        if document_type not in ["document", "multi-document", "conversation"]:
            raise ValueError("Invalid document type")

        return self._import_folder(data, document_type)

    def check_data(self, data, document_type):
        if data["metadata"]["resource_type"] != "directory":
            self._invalid_reason = "Resource type is not directory"
            return False

        return True

    def _import_folder(
        self, data, document_type
    ) -> Union[list[Document], list[MultiDocument]]:
        match document_type:
            case "document":
                return self._create_documents(data)
            case "multi-document":
                raise NotImplementedError("Multi-document not yet implemented")
            case "conversation":
                raise NotImplementedError("Conversation not yet implemented")

    @staticmethod
    def _create_documents(data) -> Union[list[Document], list[MultiDocument]]:
        documents = []
        for document in data["data"]:
            documents.append(FolderConnector._create_document(document))

        return documents

    @staticmethod
    def _create_document(data) -> Document:
        if data["metadata"]["resource_type"] != "subdirectory":
            raise InvalidResourceError("Invalid resource type")

        if len(data["data"]) > 2:
            raise InvalidResourceError("Too many data objects")

        text = None
        summary = None
        for item in data["data"]:
            if item["metadata"]["data_kind"] == "text":
                text = item["data"]
            if item["metadata"]["data_kind"] == "summary":
                summary = item["data"]

        return Document(text, summary)
