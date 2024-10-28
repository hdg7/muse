import torch
from transformers import pipeline

from muse.summarizer.summarizer import Summarizer
from muse.utils.decorators import with_valid_options


class Conversation(Summarizer):
    @with_valid_options(
        device={
            "type": str,
            "default": "cuda" if torch.cuda.is_available() else "cpu",
            "help": "The device to use",
        },
    )
    def __init__(self, options: dict[str, any]):
        if options is None:
            options = {}
        self.device = options.get(
            "device", "cuda" if torch.cuda.is_available() else "cpu"
        )
        if self.device == "cuda":
            try:
                self.summarizer = pipeline(
                    "summarization",
                    model="kabita-choudhary/finetuned-bart-for-conversation-summary",
                    device=0,
                )
            except:
                self.summarizer = pipeline(
                    "summarization",
                    model="kabita-choudhary/finetuned-bart-for-conversation-summary",
                )
        else:
            self.summarizer = pipeline(
                "summarization",
                model="kabita-choudhary/finetuned-bart-for-conversation-summary",
            )

    def summarize(self, texts) -> list[str]:
        if isinstance(texts, list):
            return self._summary_multi(texts)
        return [self._summarize_single(texts[0])]

    def _summarize_single(self, text):
        return self.summarizer(text.text)[0]["summary_text"]

    def _summary_multi(self, texts):
        return [self._summarize_single(text) for text in texts]
