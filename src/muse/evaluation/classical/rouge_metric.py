from rouge import Rouge

from muse.evaluation.evaluation import Evaluation


class RougeMetric(Evaluation):
    """
    Class to evaluate the ROUGE metric

    ROUGE only applies to comparing summaries and reference summaries
    """
    def __init__(self, params):
        self.rouge = Rouge()
        self.avg = params.get("avg", False)

    def evaluate(self, summary, reference_text=None, reference_summary=None) -> dict[str, any]:
        """
        Method to evaluate the summary

        :param summary: The summary to be evaluated
        :param reference_text: The reference text is not used in ROUGE evaluation
        :param reference_summary: The reference summary to compare the summary to (optional)
        :return: The evaluation results
        """
        if len(summary) != len(reference_summary):
            raise ValueError("The number of summaries and reference summaries should be the same")

        if len(summary) == 1:
            return self._evaluate_single(summary[0], reference_summary[0])
        else:
            return self._evaluate_multi(summary, reference_summary)

    def _evaluate_single(self, summary, reference_summary):
        rouge_score = self.rouge.get_scores(str(summary), str(reference_summary))
        return {
            "rouge_score": rouge_score,
        }

    def _evaluate_multi(self, summary, reference_summary):
        summary = [str(s) for s in summary]
        reference_summary = [str(rs) for rs in reference_summary]
        rouge_score = self.rouge.get_scores(summary, reference_summary, avg=self.avg)
        return {
            "rouge_score": rouge_score,
        }
