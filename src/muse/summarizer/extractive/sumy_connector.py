from nltk import download
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer

from muse.summarizer.summarizer import Summarizer


class Sumy(Summarizer):
    def __init__(self, params):
        super().__init__(params)
        download("punkt_tab")

    def summarize(self, texts) -> list[str]:
        if isinstance(texts, list):
            return self._summary_multi(texts)
        return [self._summarize_single(texts[0])]

    @staticmethod
    def _summarize_single(text):
        parser = PlaintextParser.from_string(str(text), Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 1)
        return str(summary[0])

    def _summary_multi(self, texts):
        return [self._summarize_single(text) for text in texts]
