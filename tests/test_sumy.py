# An example of an object using sumy to summarize text
# This is a simple example of how to use gensim to summarize text

# From this python package we import the specific modules we need

import nltk
from muse.system.extractive.sumy_connector import Sumy


class TestSumy:
    def test_summarize(self):
        nltk.download("punkt")
        nltk.download("punkt_tab")
        text = "This is a long text that needs to be summarized. It is very long and boring. I am trying to make it shorter. Maybe we can try to write something a little bit longer."
        sumy = Sumy(text)
        summary = sumy.summarize()
        print(summary[0])
        assert str(summary[0]) == "Maybe we can try to write something a little bit longer."

