class Document:
    def __init__(self, text: str, metadata: dict):
        self.text = text
        self.metadata = metadata

    def __str__(self):
        return str(self.text)
