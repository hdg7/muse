from nltk.translate.bleu_score import corpus_bleu

from muse.evaluation.evaluation import Evaluation


class BleuMetric(Evaluation):
    """
    Class to evaluate the BLEU metric

    BLEU only applies to comparing summaries and reference summaries
    """

    def __init__(self, args):
        self.args = args

    def evaluate(self, summary, reference_text=None, reference_summary=None) -> dict[str, any]:
        if len(summary) != len(reference_summary):
            raise ValueError("The number of summaries and reference summaries should be the same")

        if len(summary) == 1:
            return self._evaluate_single(summary[0], reference_summary[0])
        else:
            return self._evaluate_multi(summary, reference_summary)

    @staticmethod
    def _evaluate_single(summary, reference_summary):
        bleu_score = corpus_bleu([str(reference_summary)], [str(summary)])
        return {
            "bleu_score": bleu_score,
        }

    @staticmethod
    def _evaluate_multi(summary, reference_summary):
        summary = [str(s) for s in summary]
        reference_summary = [[str(rs)] for rs in reference_summary]
        bleu_score = corpus_bleu(reference_summary, summary)
        return {
            "bleu_score": bleu_score,
        }
