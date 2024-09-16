from nltk.translate import meteor
from nltk import word_tokenize

from muse.evaluation.evaluation import Evaluation


class MeteorMetric(Evaluation):
    """
    Class to evaluate the METEOR metric

    METEOR only applies to comparing summaries and reference summaries
    """
    def __init__(self, params):
        pass

    def evaluate(self, summary, reference_text=None, reference_summary=None) -> dict[str, any]:
        if len(summary) != len(reference_summary):
            raise ValueError("The number of summaries and reference summaries should be the same")

        if len(summary) == 1:
            return self._evaluate_single(summary[0], reference_summary[0])
        else:
            return self._evaluate_multi(summary, reference_summary)

    @staticmethod
    def _evaluate_single(summary, reference_summary):
        meteor_score = meteor(word_tokenize(str(summary)), word_tokenize(str(reference_summary)))
        return {
            "meteor_scores": meteor_score,
            "meteor": meteor_score
        }

    @staticmethod
    def _evaluate_multi(summary, reference_summary):
        summary = [word_tokenize(str(s)) for s in summary]
        reference_summary = [word_tokenize(str(rs)) for rs in reference_summary]
        meteor_score = [meteor(s, rs) for s, rs in zip(summary, reference_summary)]
        return {
            "meteor_scores": meteor_score,
            "meteor": sum(meteor_score) / len(meteor_score)
        }