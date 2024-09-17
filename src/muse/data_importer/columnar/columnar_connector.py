from io import BytesIO, StringIO

import pandas as pd

from muse.data_importer.data_importer import Importer
from muse.data_manager.conversation.conversation import Conversation
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.utils.resource_errors import InvalidResourceError


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

    def __init__(self, options: dict[str, any] = None):
        self._invalid_reason = None

        self.text_column = options.get("text_column", "text")
        self.summary_column = options.get("summary_column", "summary")

        self.metadata_columns = options.get("metadata_columns", [])

        self.csv_separator = options.get("csv_separator", ",")

    def import_data(self, data, document_type):
        if not self.check_data(data, document_type):
            raise InvalidResourceError("Invalid data", self._invalid_reason)

        if document_type not in ["document", "multi-document", "conversation"]:
            raise ValueError("Invalid document type")

        if data["metadata"]["resource_type"] == "csv":
            return self._import_csv(data, document_type)

        if data["metadata"]["resource_type"] == "parquet":
            return self._import_parquet(data, document_type)

    def check_data(self, data, document_type):
        if data["metadata"]["resource_type"] not in ["csv", "parquet"]:
            self._invalid_reason = "File type is not csv or parquet"
            return False

        return True

    def _import_csv(self, data, document_type):
        if document_type == "document":
            return self._create_documents(
                pd.read_csv(StringIO(data["data"]), sep=self.csv_separator)
            )
        if document_type == "multi-document":
            return self._create_multi_document_csv(
                pd.read_csv(StringIO(data["data"]), sep=self.csv_separator)
            )
        if document_type == "conversation":
            return self._create_conversation_csv(
                pd.read_csv(StringIO(data["data"]), sep=self.csv_separator)
            )

    def _import_parquet(self, data, document_type):
        if document_type == "document":
            return self._create_documents(
                pd.read_parquet(BytesIO(data["data"]))
            )
        if document_type == "multi-document":
            return self._create_multi_document_csv(
                pd.read_parquet(BytesIO(data["data"]))
            )
        if document_type == "conversation":
            return self._create_conversation_csv(
                pd.read_parquet(BytesIO(data["data"]))
            )

    def _create_documents(self, df: pd.DataFrame):
        if self.text_column not in df.columns:
            raise InvalidResourceError(
                f"No '{self.text_column}' column found, please rename the text column to '{self.text_column}', and if "
                f"you have a summary, rename that to '{self.summary_column}', or set the text_column and summary_column"
            )
        documents = []
        for i, row in df.iterrows():
            text = row[self.text_column]
            summary = row.get(self.summary_column, None)
            if self.metadata_columns:
                metadata = {col: row[col] for col in self.metadata_columns}
            else:
                metadata = {k: v for k, v in row.items() if k not in ["text", "summary"]}
            documents.append(Document(text, summary, metadata))
        return documents

    def _create_multi_document_csv(self, df: pd.DataFrame):
        raise NotImplementedError

    def _create_conversation_csv(self, df: pd.DataFrame):
        raise NotImplementedError
