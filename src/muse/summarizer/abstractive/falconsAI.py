from transformers import pipeline
import torch

from muse.summarizer.summarizer import Summarizer

class FalconsAI(Summarizer):
    def __init__(self, params):
        super().__init__(params)
        self.device = params.get(
            "device", "cuda" if torch.cuda.is_available() else "cpu"
        )
        if self.device == "cuda":
            try:
                self.summarizer = pipeline("summarization", model="Falconsai/text_summarization",device=0)
            except:
                self.summarizer = pipeline("summarization", model="Falconsai/text_summarization")
        else:
            self.summarizer = pipeline("summarization", model="Falconsai/text_summarization")


    def summarize(self, texts) -> list[str]:
        if isinstance(texts, list):
            return self._summary_multi(texts)
        return [self._summarize_single(texts[0])]

    def _summarize_single(self, text):
        return self.summarizer(text.text)[0]["summary_text"]

    def _summary_multi(self, texts):
        return [self._summarize_single(text) for text in texts]
