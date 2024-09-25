from nltk import download, word_tokenize
from nltk.translate.bleu_score import corpus_bleu

from muse.evaluation.evaluation import Evaluation


class BleuMetric(Evaluation):
    """
    Class to evaluate the BLEU metric

    BLEU only applies to comparing summaries and reference summaries
    """

    def __init__(self, args):
        download("punkt_tab")
        self.args = args

    def evaluate(
        self, summary, reference_text=None, reference_summary=None
    ) -> dict[str, any]:
        if len(summary) != len(reference_summary):
            raise ValueError(
                "The number of summaries and reference summaries should be the same"
            )

        if len(summary) == 1:
            return self._evaluate_single(summary[0], reference_summary[0])
        else:
            return self._evaluate_multi(summary, reference_summary)

    @staticmethod
    def _evaluate_single(summary, reference_summary):
        summary = [word_tokenize(str(summary))]
        reference_summary = [[word_tokenize(str(reference_summary))]]
        bleu_score = corpus_bleu(reference_summary, summary)
        return {
            "bleu_score": bleu_score,
        }

    @staticmethod
    def _evaluate_multi(summary, reference_summary):
        summary = [word_tokenize(str(s)) for s in summary]
        reference_summary = [[word_tokenize(str(rs))] for rs in reference_summary]
        bleu_score = corpus_bleu(reference_summary, summary)
        return {
            "bleu_score": bleu_score,
        }


if __name__ == "__main__":
    # hyp1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
    #         'ensures', 'that', 'the', 'military', 'always',
    #         'obeys', 'the', 'commands', 'of', 'the', 'party']
    # ref1a = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
    #          'ensures', 'that', 'the', 'military', 'will', 'forever',
    #          'heed', 'Party', 'commands']
    # ref1b = ['It', 'is', 'the', 'guiding', 'principle', 'which',
    #          'guarantees', 'the', 'military', 'forces', 'always',
    #          'being', 'under', 'the', 'command', 'of', 'the', 'Party']
    # ref1c = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
    #          'army', 'always', 'to', 'heed', 'the', 'directions',
    #          'of', 'the', 'party']
    # hyp2 = ['he', 'read', 'the', 'book', 'because', 'he', 'was',
    #         'interested', 'in', 'world', 'history']
    # ref2a = ['he', 'was', 'interested', 'in', 'world', 'history',
    #          'because', 'he', 'read', 'the', 'book']
    # list_of_references = [[ref1a, ref1b, ref1c], [ref2a]]
    # hypotheses = [hyp1, hyp2]
    hyp1 = [
        "This",
        "is",
        "a",
        "long",
        "text",
        "that",
        "needs",
        "to",
        "be",
        "summarized",
        ".",
        "It",
        "is",
        "very",
        "long",
        "and",
        "boring",
        ".",
        "I",
        "am",
        "trying",
        "to",
        "make",
        "it",
        "shorter",
        ".",
        "Maybe",
        "we",
        "can",
        "try",
        "to",
        "write",
        "something",
        "a",
        "little",
        "bit",
        "longer",
        ".",
    ]
    ref1 = [
        "This",
        "is",
        "a",
        "long",
        "text",
        "that",
        "needs",
        "to",
        "be",
        "summarized",
        ".",
        "It",
        "is",
        "very",
        "long",
        "and",
        "boring",
        ".",
        "I",
        "am",
        "trying",
        "to",
        "make",
        "it",
        "shorter",
        ".",
        "Maybe",
        "we",
        "can",
        "try",
        "to",
        "write",
        "something",
        "a",
        "little",
        "bit",
        "longer",
        ".",
    ]
    list_of_references = [[ref1]]
    hypotheses = [hyp1]
    print(corpus_bleu(list_of_references, hypotheses))
