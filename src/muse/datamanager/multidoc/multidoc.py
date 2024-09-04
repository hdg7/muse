from ..singledoc.singledoc import Document


class MultiDocument:
    def __init__(self, documents: Document, metadata: dict):
        self.documents = documents
        self.metadata = metadata

    def __str__(self):
        return str(self.documents)
