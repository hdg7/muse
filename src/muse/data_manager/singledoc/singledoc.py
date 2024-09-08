class Document:
    def __init__(self, text: str, summary: str | None = None, metadata: dict | None = None):
        self.text = text
        self.summary = summary
        self.metadata = metadata

    def __str__(self):
        return str(self.text)
