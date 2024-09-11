from muse.data_manager.document.document import Document


class MultiDocument:
    def __init__(
        self,
        documents: list[Document],
        summary: str | None = None,
        metadata: dict | None = None,
    ):
        self.documents = documents
        self.summary = summary
        self.metadata = metadata

    def __str__(self):
        return str(self.documents)
