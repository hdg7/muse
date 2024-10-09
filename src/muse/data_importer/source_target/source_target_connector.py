import os

from muse.data_importer.data_importer import Importer, split_text_by_regex
from muse.data_importer.fetcher import get_resource_type, handle_uri
from muse.data_manager.conversation.conversation import Conversation, TextUnit
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument


class SourceTargetConnector(Importer):
    """
    SourceTargetConnector is a class that imports data from a Source-Target file pair.

    The data path is either expected to be a dir containing one or more pairs of .source and .target files,
    or a single file (either .source or .target), where the other file is expected to be in the same directory.
    """

    def __init__(self, options: dict[str, any] = None):
        if options is None:
            options = {}

        self.separator = options.get("separator", "\n")

        self.multi_document_delimiter = options.get(
            "multi_document_delimiter", "#DOCUMENT#"
        )
        self.conversation_delimiter = options.get("conversation_separator", r"#\w+#")

    def import_data(self, data_path, document_type):
        if not self.check_data(data_path, document_type):
            raise ValueError("Invalid data path")

        _data_path = handle_uri(data_path)
        data_type = get_resource_type(_data_path)

        if data_type == "file":
            if data_path.endswith(".source"):
                source_path = _data_path
                target_path = data_path.replace(".source", ".target")
            else:
                target_path = _data_path
                source_path = data_path.replace(".target", ".source")
            with open(source_path, "r") as source_file, open(
                target_path, "r"
            ) as target_file:
                source = source_file.read()
                target = target_file.read()
                meta = os.path.basename(source_path)
            files = [(source, target, meta)]
        else:
            files = []
            for root, dirs, f in os.walk(_data_path):
                source_files = [f for f in f if f.endswith(".source")]
                for source_file in source_files:
                    target_file = source_file.replace(".source", ".target")
                    with open(os.path.join(root, source_file), "r") as s, open(
                        os.path.join(root, target_file), "r"
                    ) as t:
                        source = s.read()
                        target = t.read()
                        meta = os.path.basename(source_file)
                    files.append((source, target, meta))

        return self._import_source_docs(files, document_type)

    def check_data(self, data_path, document_type):
        _data_path = handle_uri(data_path)
        data_type = get_resource_type(_data_path)
        if data_type == "directory":
            for root, dirs, files in os.walk(_data_path):
                source_files = [f for f in files if f.endswith(".source")]
                target_files = [f for f in files if f.endswith(".target")]
                if len(source_files) != len(target_files):
                    return False
                for source_file in source_files:
                    target_file = source_file.replace(".source", ".target")
                    if target_file not in target_files:
                        return False
        elif data_type == "file":
            if not _data_path.endswith(".source") and not _data_path.endswith(
                ".target"
            ):
                return False
            else:
                if data_path.endswith(".source"):
                    other_file = data_path.replace(".source", ".target")
                else:
                    other_file = data_path.replace(".target", ".source")

                other_path = handle_uri(other_file)
                other_type = get_resource_type(other_path)
                if other_type != "file":
                    return False
        else:
            return False

        return True

    def _import_source_docs(self, files, document_type):
        if document_type == "conversation":
            return self._import_conversations(files)
        elif document_type == "multi_document":
            return self._import_multi_document(files)
        else:
            return self._import_single_document(files)

    def _import_single_document(self, files):
        documents = []
        for source, target, meta in files:
            source_documents = source.split(self.separator)
            target_documents = target.split(self.separator)
            assert len(source_documents) == len(target_documents)
            for i, (s, t) in enumerate(zip(source_documents, target_documents)):
                documents.append(Document(s, t, {"resource_name": f"{meta}-{i}"}))

        return documents

    def _import_multi_document(self, files):
        multi_documents = []
        for source, target, meta in files:
            source_documents = source.split(self.separator)
            target_documents = target.split(self.separator)
            assert len(source_documents) == len(target_documents)
            for i, (s, t) in enumerate(zip(source_documents, target_documents)):
                docs = s.split(self.multi_document_delimiter)
                multi_documents.append(
                    MultiDocument(
                        [Document(d, t) for d in docs if d],
                        t,
                        {"resource_name": f"{meta}-{i}"},
                    )
                )

        return multi_documents

    def _import_conversations(self, files):
        conversations = []
        for source, target, meta in files:
            source_documents = source.split(self.separator)
            target_documents = target.split(self.separator)
            assert len(source_documents) == len(target_documents)
            for i, (s, t) in enumerate(zip(source_documents, target_documents)):
                conversation_units = split_text_by_regex(s, self.conversation_delimiter)
                conversations.append(
                    Conversation(
                        [
                            TextUnit(unit[1], unit[0])
                            for unit in conversation_units
                            if unit
                        ],
                        t,
                        {"resource_name": f"{meta}-{i}"},
                    )
                )

        return conversations
