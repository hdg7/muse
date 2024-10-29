from muse.data_manager import Document
from muse.summarizer import Spacy


def test_summarize():
    text = Document(
        "This is a long text that needs to be summarized. It is very long and boring. I am trying to "
        "make it shorter. Maybe we can try to write something a little bit longer."
    )
    spacy = Spacy({})
    summary = spacy.summarize([text])
    assert (
        str(summary[0])
        == "This is a long text that needs to be summarized. Maybe we can try to write something a little bit longer. It is very long and boring."
    )
