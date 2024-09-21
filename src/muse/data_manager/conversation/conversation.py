class TextUnit:
    def __init__(self, text: str, speaker: str, metadata: dict | None = None):
        self.text = text
        self.speaker = speaker
        self.metadata = metadata

    def __str__(self):
        return f"{str(self.speaker)}: {str(self.text)}"


class Conversation:
    def __init__(
        self,
        text_units: list[TextUnit],
        summary: str | None = None,
        metadata: dict | None = None,
    ):
        self.text_units = text_units
        self.summary = summary
        self.metadata = metadata

    def __str__(self):
        return "\n".join([str(text_unit) for text_unit in self.text_units])
