#An example of an object using sumy to summarize text
# This is a simple example of how to use gensim to summarize text

#From this python package we import the specific modules we need


import unittest
import sys
import os
import nltk

try:
        home = os.environ["MUSE_HOME"]
except KeyError:
        home = os.environ["HOME"]
        home += "/muse"
sys.path.append(home)

from muse.system.extractive.sumyMuse import Sumy

class TestGensim(unittest.TestCase):

    def test_summarize(self):
        nltk.download('punkt')
        nltk.download('punkt_tab')
        text = "This is a long text that needs to be summarized. It is very long and boring. I am trying to make it shorter. Maybe we can try to write something a little bit longer."
        sumy = Sumy(text)
        smry = sumy.summarize()  
        self.assertEqual(summary, "This is a long text that needs to be summarized.")


if __name__ == '__main__':
    unittest.main()
