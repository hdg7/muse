# An example of an object using sumy to summarize text
# This is a simple example of how to use gensim to summarize text

# From this python package we import the specific modules we need


import unittest

from utils import setup

setup()

from src.muse.system.extractive.gensimMuse import Gensim


class TestGensim(unittest.TestCase):

    def test_summarize(self):
        text = "This is a long text that needs to be summarized. It is very long and boring. I am trying to make it shorter. Maybe we can try to write something a little bit longer."
        gensim = Gensim(text)
        summary = gensim.summarize()
        self.assertEqual(summary, "This is a long text that needs to be summarized.")

    def test_get_keywords(self):
        text = "This is a long text that needs to be summarized. It is very long and boring. I am trying to make it shorter. Maybe we can try to write something a little bit longer."
        gensim = Gensim(text)
        keywords = gensim.get_keywords()
        self.assertEqual(keywords, "long text")


if __name__ == "__main__":
    unittest.main()