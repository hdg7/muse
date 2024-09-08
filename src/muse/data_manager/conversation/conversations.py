

class TextUnit:
    def __init__(self, text: str, metadata: dict | None = None):
        self.text = text
        self.metadata = metadata

    def __str__(self):
        return str(self.text)


class Conversation:
    def __init__(self, text_units: list[TextUnit], summary: str | None = None, metadata: dict | None = None):
        self.text_units = text_units
        self.summary = summary
        self.metadata = metadata

    def __str__(self):
        return str(self.text_units)
