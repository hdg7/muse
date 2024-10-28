from nltk import download
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer

from muse.summarizer.summarizer import Summarizer
from muse.utils.decorators import with_valid_options


class Sumy(Summarizer):
    @with_valid_options()
    def __init__(self, options):
        if not options:
            options = {}
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
        if len(summary) == 0:
            return ""
        return str(summary[0])

    def _summary_multi(self, texts):
        return [self._summarize_single(text) for text in texts]
