# An example of an object using sumy to summarize text
# This is a simple example of how to use gensim to summarize text

# import nltk
# from gensim.summarization import keywords, summarize

from muse.summarizer.summarizer import Summarizer


class Gensim(Summarizer):
    def summarize(self, text):
        pass
        # summary = summarize(str(self.text))
        # return summary

    def get_keywords(self):
        pass
        # return keywords(str(self.text))
