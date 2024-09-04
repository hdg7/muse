# An example of an object using sumy to summarize text
# This is a simple example of how to use sumy to summarize text

import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from ..summarizer import Summarizer


class Sumy(Summarizer):
    def summarize(self) -> str:
        parser = PlaintextParser.from_string(str(self.text), Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 1)
        return summary


# Example usage
# text = "This is a long text that needs to be summarized. It is very long and boring. I am trying to make it shorter."
# sumy = Sumy(text)
# summary = sumy.summarize()
# for sentence in summary:
#     print(sentence)

# print(summary)
