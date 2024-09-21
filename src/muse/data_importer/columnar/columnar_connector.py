from io import BytesIO

import pandas as pd

from muse.data_importer.data_importer import Importer, split_text_by_regex
from muse.data_importer.fetcher import get_resource_type, handle_uri
from muse.data_manager.conversation.conversation import Conversation, TextUnit
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
        - Each row is assumed to be a separate document, with an id column named 'multi_doc_id', used to group documents together.
        - All else is the same as for Document.

    For conversation (not yet implemented):
        - We assume same format as Document, but within the text, we have a conversation.
        - Each person is delineated by #PERSON# <text>, e.g.
            #PERSON1# Hello, how are you?
            #PERSON2# I'm good, how are you?
    """

    def __init__(self, options: dict[str, any] = None):
        self._invalid_reason = None

        if options is None:
            options = {}

        self.text_column = options.get("text_column", "text")
        self.summary_column = options.get("summary_column", "summary")

        self.metadata_columns = options.get("metadata_columns", [])

        self.csv_separator = options.get("csv_separator", ",")

        self.multi_doc_id_column = options.get("multi_doc_id_column", "multi_doc_id")
        self.multi_document_delimiter = options.get(
            "multi_document_delimiter", "#DOCUMENT#"
        )
        self.conversation_delimiter = options.get("conversation_separator", r"#\w+#")

    def import_data(self, data_path, document_type):
        if not self.check_data(data_path, document_type):
            raise InvalidResourceError("Invalid data", self._invalid_reason)

        if document_type not in ["document", "multi-document", "conversation"]:
            raise ValueError("Invalid document type")

        data_path = handle_uri(data_path)
        data_type = get_resource_type(data_path)

        data = self._read_data(data_path)

        if data_type == "csv":
            return self._import_csv(data, document_type)

        if data_type == "parquet":
            return self._import_parquet(data, document_type)

    def check_data(self, data_path, document_type):
        if get_resource_type(handle_uri(data_path)) not in ["csv", "parquet"]:
            self._invalid_reason = "File type is not csv or parquet"
            return False

        return True

    @staticmethod
    def _read_data(data_path):
        with open(data_path, "rb") as file:
            return BytesIO(file.read())

    def _import_csv(self, data, document_type):
        if document_type == "document":
            return self._create_documents(pd.read_csv(data, sep=self.csv_separator))
        if document_type == "multi-document":
            return self._create_multi_document_csv(
                pd.read_csv(data, sep=self.csv_separator)
            )
        if document_type == "conversation":
            return self._create_conversation_csv(
                pd.read_csv(data, sep=self.csv_separator)
            )

    def _import_parquet(self, data, document_type):
        if document_type == "document":
            return self._create_documents(pd.read_parquet(data))
        if document_type == "multi-document":
            return self._create_multi_document_csv(pd.read_parquet(data))
        if document_type == "conversation":
            return self._create_conversation_csv(pd.read_parquet(data))

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
                metadata = {
                    k: v for k, v in row.items() if k not in ["text", "summary"]
                }
            documents.append(Document(text, summary, metadata))
        return documents

    def _create_multi_document_csv(self, df: pd.DataFrame):
        if self.text_column not in df.columns:
            raise InvalidResourceError(
                f"No '{self.text_column}' column found, please rename the text column to '{self.text_column}', and if "
                f"you have a summary, rename that to '{self.summary_column}', or set the text_column and summary_column"
            )
        multidocs = []

        if self.multi_doc_id_column in df.columns:
            for i, group in df.groupby(self.multi_doc_id_column):
                group_dict = group.to_dict(orient="list")
                texts = group_dict[self.text_column]
                summaries = group_dict[self.summary_column]
                summary = next((s for s in summaries if s is not None), None)
                if self.metadata_columns:
                    metadata = {col: group_dict[col] for col in self.metadata_columns}
                else:
                    metadata = {
                        k: v
                        for k, v in group_dict.items()
                        if k not in ["text", "summary"]
                    }
                multidocs.append(
                    MultiDocument(
                        [Document(t, None, None) for t in texts], summary, metadata
                    )
                )
        else:
            for i, row in df.iterrows():
                text = row[self.text_column].split(self.multi_document_delimiter)
                summary = row.get(self.summary_column, None)
                if self.metadata_columns:
                    metadata = {col: row[col] for col in self.metadata_columns}
                else:
                    metadata = {
                        k: v for k, v in row.items() if k not in ["text", "summary"]
                    }
                multidocs.append(
                    MultiDocument(
                        [Document(t, None, None) for t in text], summary, metadata
                    )
                )
        return multidocs

    def _create_conversation_csv(self, df: pd.DataFrame):
        if self.text_column not in df.columns:
            raise InvalidResourceError(
                f"No '{self.text_column}' column found, please rename the text column to '{self.text_column}', and if "
                f"you have a summary, rename that to '{self.summary_column}', or set the text_column and summary_column"
            )
        conversations = []
        for i, row in df.iterrows():
            text = row[self.text_column]
            summary = row.get(self.summary_column, None)
            if self.metadata_columns:
                metadata = {col: row[col] for col in self.metadata_columns}
            else:
                metadata = {
                    k: v for k, v in row.items() if k not in ["text", "summary"]
                }
            conversation_units = split_text_by_regex(text, self.conversation_delimiter)
            text_units = []
            for unit in conversation_units:
                text_units.append(TextUnit(unit[1], unit[0]))
            conversations.append(Conversation(text_units, summary, metadata))
        return conversations
