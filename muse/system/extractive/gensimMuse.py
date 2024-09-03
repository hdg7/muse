#An example of an object using sumy to summarize text
# This is a simple example of how to use gensim to summarize text

import nltk
from gensim.summarization import summarize
from gensim.summarization import keywords

class Gensim:
    def __init__(self, text):
        self.text = text

    def summarize(self):
        summary = summarize(self.text)
        return summary

    def get_keywords(self):
        return keywords(self.text)


