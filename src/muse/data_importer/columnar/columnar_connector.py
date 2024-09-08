import pandas as pd

from ...data_manager import Conversation, Document, MultiDocument
from ...utils import InvalidResourceError
from ..data_importer import Importer


class ColumnarConnector(Importer):
    """
    Class for importing data from Columnar files.

    For Document:
        - The text is assumed to be in a column named 'text'.
        - the summary, if present, is assumed to be in a column named 'summary'.
        - all other columns are assumed to be metadata.

    For MultiDocument:
        - Each row is assumed to be a separate document, with an id column named 'id', used to group documents together.
        - All else is the same as for Document.

    For conversation (not yet implemented):
        - We assume same format as Document, but within the text, we have a conversation.
        - Each person is delineated by #PERSON# <text>, e.g.
            #PERSON1# Hello, how are you?
            #PERSON2# I'm good, how are you?
    """

    def __init__(self):
        self._invalid_reason = None

    def import_data(self, data, document_type):
        if not self.check_data(data, document_type):
            raise InvalidResourceError("Invalid data", self._invalid_reason)

        if document_type not in ["document", "multi-document", "conversation"]:
            raise ValueError("Invalid document type")

        if data.metadata["file_type"] == "csv":
            return ColumnarConnector._import_csv(data, document_type)

        if data.metadata["file_type"] == "parquet":
            return ColumnarConnector._import_parquet(data, document_type)

    def check_data(self, data, document_type):
        if data.metadata["file_type"] not in ["csv", "parquet"]:
            self._invalid_reason = "File type is not csv or parquet"
            return False

        # TODO: Check more things about the data
        return True

    @staticmethod
    def _import_csv(data, document_type):
        if document_type == "document":
            return ColumnarConnector._create_documents(pd.read_csv(data.content))
        if document_type == "multi-document":
            return ColumnarConnector._create_multi_document_csv(
                pd.read_csv(data.content)
            )
        if document_type == "conversation":
            return ColumnarConnector._create_conversation_csv(pd.read_csv(data.content))

    @staticmethod
    def _import_parquet(data, document_type):
        if document_type == "document":
            return ColumnarConnector._create_documents(pd.read_parquet(data.content))
        if document_type == "multi-document":
            return ColumnarConnector._create_multi_document_csv(
                pd.read_parquet(data.content)
            )
        if document_type == "conversation":
            return ColumnarConnector._create_conversation_csv(
                pd.read_parquet(data.content)
            )

    @staticmethod
    def _create_documents(df: pd.DataFrame):
        documents = []
        for i, row in df.iterrows():
            text = row["text"]
            summary = row.get("summary", None)
            metadata = {k: v for k, v in row.items() if k not in ["text", "summary"]}
            documents.append(Document(text, summary, metadata))
        return documents

    @staticmethod
    def _create_multi_document_csv(df: pd.DataFrame):
        raise NotImplementedError

    @staticmethod
    def _create_conversation_csv(df: pd.DataFrame):
        raise NotImplementedError
