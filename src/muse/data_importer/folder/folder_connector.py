import os
import re
from typing import Union

import pandas as pd

from muse.data_importer.data_importer import Importer, split_text_by_regex
from muse.data_importer.fetcher import get_resource_type, handle_uri
from muse.data_manager.conversation.conversation import Conversation, TextUnit
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

    def __init__(self, options: dict[str, any] = None):
        self._invalid_reason = None

        if options is None:
            options = {}

        self.summary_suffix = options.get("summary_suffix", "_summary")
        self.metadata_suffix = options.get("metadata_suffix", "_metadata")

        self.summary_file = options.get("summary_file", "summary")
        self.metadata_file = options.get("metadata_file", "metadata")

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

        data = self._read_data(data_path)

        return self._import_folder(data, document_type)

    def check_data(self, data_path, document_type):
        data_path = handle_uri(data_path)
        data_type = get_resource_type(data_path)
        if data_type == "directory":
            files = os.listdir(data_path)
            if any(
                [
                    f.endswith(".source") or f.endswith(".target")
                    for f in files
                    if os.path.isfile(os.path.join(data_path, f))
                ]
            ):
                self._invalid_reason = "Directory contains .source or .target files, so is not valid for the folder connector"
                return False
            return True
        return False

    def _read_data(self, data_path):
        df = pd.DataFrame()
        files = os.listdir(data_path)

        for identifier in [
            f
            for f in files
            if (self.summary_suffix not in f and self.metadata_suffix not in f)
            and os.path.isfile(os.path.join(data_path, f))
        ]:
            identifier_no_extension = identifier.rsplit(".", 1)[0]
            summary = rf"{re.escape(identifier_no_extension)}{re.escape(self.summary_suffix)}.*"
            if any([re.match(summary, f) for f in files]):
                summary = [f for f in files if re.match(summary, f)][0]
                summary = os.path.join(data_path, f"{summary}")
                with open(summary, "r") as file:
                    summary_data = file.read()
            else:
                summary_data = None

            metadata = rf"{re.escape(identifier_no_extension)}{re.escape(self.metadata_suffix)}.json"
            if any([re.match(metadata, f) for f in files]):
                metadata = [f for f in files if re.match(metadata, f)][0]
                metadata = os.path.join(data_path, f"{metadata}")
                metadata_df = pd.read_json(metadata)
            else:
                metadata_df = pd.DataFrame()

            with open(os.path.join(data_path, identifier), "r") as file:
                text_data = file.read()

            text_data = text_data.split(self.multi_document_delimiter)

            data = {
                "id": [identifier for _ in range(len(text_data))],
                "text": text_data,
                "summary": [summary_data for _ in range(len(text_data))],
                **metadata_df,
                "resource_name": [identifier for _ in range(len(text_data))],
            }
            frame = pd.DataFrame(data)
            df = pd.concat([df, frame])

        for identifier in [
            f for f in files if os.path.isdir(os.path.join(data_path, f))
        ]:
            summary = rf"{re.escape(self.summary_file)}.*"
            files_in_identifier = os.listdir(os.path.join(data_path, identifier))
            if any([re.match(summary, f) for f in files_in_identifier]):
                summary = [f for f in files_in_identifier if re.match(summary, f)][0]
                summary = os.path.join(data_path, identifier, f"{summary}")
                with open(summary, "r") as file:
                    summary_data = file.read()
            else:
                summary_data = None

            metadata = os.path.join(data_path, identifier, self.metadata_file)
            metadata = rf"{re.escape(metadata)}.json"
            if any([re.match(metadata, f) for f in files_in_identifier]):
                metadata = [f for f in files_in_identifier if re.match(metadata, f)][0]
                metadata = os.path.join(data_path, identifier, f"{metadata}")
                metadata_df = pd.read_json(metadata)
            else:
                metadata_df = pd.DataFrame()

            text_data = []
            for file in [
                f
                for f in files_in_identifier
                if self.summary_file not in f and self.metadata_file not in f
            ]:
                with open(os.path.join(data_path, identifier, file), "r") as f:
                    text_data.append(f.read())

            if len(text_data) == 1:
                text_data = text_data[0].split(self.multi_document_delimiter)

            data = {
                "id": [identifier for _ in range(len(text_data))],
                "text": text_data,
                "summary": [summary_data for _ in range(len(text_data))],
                **metadata_df,
                "resource_name": [identifier for _ in range(len(text_data))],
            }
            frame = pd.DataFrame(data)
            df = pd.concat([df, frame])

        return df

    def _import_folder(
        self, data, document_type
    ) -> Union[list[Document], list[MultiDocument], list[Conversation]]:
        match document_type:
            case "document":
                return self._create_documents(data)
            case "multi-document":
                return self._create_multi_documents(data)
            case "conversation":
                return self._create_conversation(data)

    def _create_documents(self, data) -> list[Document]:
        documents = []
        for index, group in data.groupby("id"):
            group_dict = group.to_dict(orient="list")
            if len(group_dict["text"]) > 1:
                raise InvalidResourceError(
                    "Invalid data", "Each group should have only one text"
                )
            documents.append(
                self._create_document(
                    group_dict["text"][0],
                    group_dict["summary"][0],
                    {
                        col: group_dict[col][0]
                        for col in data.columns
                        if col not in ["text", "summary"]
                    },
                )
            )

        return documents

    @staticmethod
    def _create_document(text, summary, metadata) -> Document:
        return Document(text, summary, metadata)

    def _create_multi_documents(self, data) -> list[MultiDocument]:
        multidocs = []
        for index, group in data.groupby("id"):
            group_dict = group.to_dict(orient="list")
            if len(group_dict["text"]) < 1:
                raise InvalidResourceError(
                    "Invalid data", "Each row should have at least one text"
                )
            multidocs.append(
                MultiDocument(
                    [
                        self._create_document(text, None, None)
                        for text in group_dict["text"]
                    ],
                    group_dict["summary"][0],
                    {
                        col: group_dict[col][0]
                        for col in data.columns
                        if col not in ["text", "summary"]
                    },
                )
            )

        return multidocs

    def _create_conversation(self, data) -> list[Conversation]:
        conversations = []
        for index, group in data.groupby("id"):
            group_dict = group.to_dict(orient="list")
            if len(group_dict["text"]) > 1:
                raise InvalidResourceError(
                    "Invalid data", "Each group should have only one text"
                )
            text = group_dict["text"][0]
            conversation_units = split_text_by_regex(text, self.conversation_delimiter)
            conversation_units = [
                self._create_text_unit(unit) for unit in conversation_units
            ]
            conversations.append(
                Conversation(
                    conversation_units,
                    group_dict["summary"][0],
                    {
                        col: group_dict[col][0]
                        for col in data.columns
                        if col not in ["text", "summary"]
                    },
                )
            )

        return conversations

    @staticmethod
    def _create_text_unit(unit) -> TextUnit:
        return TextUnit(unit[1], unit[0])
