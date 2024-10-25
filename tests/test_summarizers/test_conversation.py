import os

#from pytest import mark

from muse.data_manager import Document
from muse.summarizer import Conversation


#@mark.skipif(os.getenv("SKIP_INTENSIVE_TESTS") == "true", reason="Skipping long tests")
def test_summarize():
    text = Document(
        """
        Richard: YouTube said 130,000 videos were removed from its platform since last year.
        Jaime: The company said it had seen false claims about Covid jabs "spill over into misinformation"
        Richard: The new policy covers long-approved vaccines, such as those against measles or hepatitis B.
        Jaime: One of the most popular videos removed was a 40-minute documentary called Plandemic.
        """
    )
    conversationsum = Conversation({})
    summary = conversationsum.summarize([text])
    return summary
    assert (
        str(summary[0])
        == 'More than 130,000 videos were removed from YouTube since last year. One of the most popular videos was a 40-minute documentary called Plandemic. YouTube has a new policy that covers long-approved vaccines, such as those against measles or hepatitis B.'
    )

test_summarize()
