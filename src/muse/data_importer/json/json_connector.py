import json
from typing import Union

from muse.data_importer.data_importer import Importer
from muse.data_importer.fetcher import get_resource_type, handle_uri
from muse.data_manager.conversation.conversation import Conversation, TextUnit
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.utils.resource_errors import InvalidResourceError


class JSONConnector(Importer):
    """
    JSONConnector is a class that imports data from a JSON file.

    It can also be used to import subdata, i.e. data stored as json within other structures such as CSV files.
    """

    def __init__(self, options: dict[str, any] = None):
        pass

    def import_data(self, data_path, document_type):
        if not self.check_data(data_path, document_type):
            raise ValueError("Invalid data path")

        data_path = handle_uri(data_path)
        with open(data_path, "r") as file:
            data = json.load(file)

        return self._import_data(data, document_type)

    def check_data(self, data_path, document_type):
        data_path = handle_uri(data_path)
        data_type = get_resource_type(data_path)
        if data_type != "file":
            return False

        try:
            with open(data_path, "r") as file:
                json.load(file)
            return True
        except json.JSONDecodeError:
            return False
        except FileNotFoundError:
            return False
        except IsADirectoryError:
            return False

    def _import_data(self, data, document_type):
        if document_type == "document":
            return self._import_document(data)
        elif document_type == "multi-document":
            return self._import_multi_document(data)
        elif document_type == "conversation":
            return self._import_conversation(data)
        else:
            raise ValueError(f"Invalid document type: {document_type}")

    @staticmethod
    def _import_document(data):
        documents = []
        for doc in data:
            text = doc.get("text", "")
            summary = doc.get("summary", "")
            meta = doc.get("meta", {})
            if not text:
                raise InvalidResourceError("Text is required for a document")
            if not isinstance(meta, dict):
                meta = {}
            documents.append(Document(text, summary, meta))

        return documents

    @staticmethod
    def _import_multi_document(data):
        multi_docs = []
        for multi_doc in data:
            summary = multi_doc.get("summary", "")
            meta = multi_doc.get("meta", {})
            documents = multi_doc.get("documents", [])
            if not isinstance(documents, list):
                raise InvalidResourceError("Documents should be a list")
            if not isinstance(meta, dict):
                meta = {}

            docs = []
            for doc in documents:
                text = doc.get("text", "")
                doc_meta = doc.get("meta", {})
                if not text:
                    raise InvalidResourceError("Text is required for a document")
                if not isinstance(doc_meta, dict):
                    doc_meta = {}
                docs.append(Document(text, "", doc_meta))

            multi_docs.append(MultiDocument(docs, summary, meta))

        return multi_docs

    @staticmethod
    def _import_conversation(data):
        conversations = []
        for conv in data:
            summary = conv.get("summary", "")
            meta = conv.get("meta", {})
            units = conv.get("conversation_units", [])
            if not isinstance(units, list):
                raise InvalidResourceError("Conversation units should be a list")
            if not isinstance(meta, dict):
                meta = {}

            conv_units = []
            for unit in units:
                text = unit.get("text", "")
                speaker = unit.get("speaker", "")
                unit_meta = unit.get("meta", {})
                if not text:
                    raise InvalidResourceError(
                        "Text is required for a conversation unit"
                    )
                if not speaker:
                    raise InvalidResourceError(
                        "Speaker is required for a conversation unit"
                    )
                if not isinstance(unit_meta, dict):
                    unit_meta = {}
                conv_units.append(TextUnit(text, speaker, unit_meta))

            conversations.append(Conversation(conv_units, summary, meta))

        return conversations

    def load_single_json(
        self, json_string: str, document_type: str
    ) -> Union[Document, MultiDocument, Conversation]:
        try:
            data = json.loads(json_string)
            data = self._import_data(data, document_type)
            if len(data) == 1:
                return data[0]
            else:
                raise InvalidResourceError("Expected a single document")
        except json.JSONDecodeError:
            raise InvalidResourceError("Invalid JSON string")

    @staticmethod
    def can_load_json(json_string: str):
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False
