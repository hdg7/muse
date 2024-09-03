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

# Example usage
text = "This is a long text that needs to be summarized. It is very long and boring. I am trying to make it shorter. Maybe we can try to write something a little bit longer."
gensim = Gensim(text)
summary = gensim.summarize()
print(text)
print(summary)
print(gensim.get_keywords())

