import os

#from pytest import mark

from muse.data_manager import Document
from muse.summarizer import FalconsAI


#@mark.skipif(os.getenv("SKIP_INTENSIVE_TESTS") == "true", reason="Skipping long tests")
def test_summarize():
    text = Document(
        """Videos that say approved vaccines are dangerous and cause autism, cancer or infertility are among those that will be taken down, the company said.  The policy includes the termination of accounts of anti-vaccine influencers.  Tech giants have been criticised for not doing more to counter false health information on their sites.  In July, US President Joe Biden said social media platforms were largely responsible for people's scepticism in getting vaccinated by spreading misinformation, and appealed for them to address the issue.  YouTube, which is owned by Google, said 130,000 videos were removed from its platform since last year, when it implemented a ban on content spreading misinformation about Covid vaccines.  In a blog post, the company said it had seen false claims about Covid jabs "spill over into misinformation about vaccines in general". The new policy covers long-approved vaccines, such as those against measles or hepatitis B.  "We're expanding our medical misinformation policies on YouTube with new guidelines on currently administered vaccines that are approved and confirmed to be safe and effective by local health authorities and the WHO," the post said, referring to the World Health Organization."""
    )
    falconssum = FalconsAI({})
    summary = falconssum.summarize([text])
    assert (
        str(summary[0])
        == 'YouTube said 130,000 videos were removed from its platform since last year . The company said it had seen false claims about Covid jabs "spill over into misinformation" The new policy covers long-approved vaccines, such as those against measles or hepatitis B .'
    )

