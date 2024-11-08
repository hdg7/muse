import bert_score

from muse.evaluation.evaluation import Evaluation
from muse.utils.decorators import with_valid_options

class BertScoreMetric(Evaluation):
    """
    Class to evaluate the BertScore metric

    BertScore only applies to comparing summaries and reference summaries
    """

    @with_valid_options(
        avg={"type": bool, "default": False, "help": "Whether to average the scores"}
    )
    def __init__(self, options):
        if not options:
            options = {}
        self.bertscore = bert_score
        if "lang" in options:
            self.lang = options["lang"]
        else:
            self.lang = "en"
        self.avg = options.get("avg", False)

    def evaluate(
        self, summary, reference_text=None, reference_summary=None
    ) -> dict[str, any]:
        """
        Method to evaluate the summary

        :param summary: The summary to be evaluated
        :param reference_text: The reference text is not used in ROUGE evaluation
        :param reference_summary: The reference summary to compare the summary to (optional)
        :return: The evaluation results
        """
        if len(summary) != len(reference_summary):
            raise ValueError(
                "The number of summaries and reference summaries should be the same"
            )

        if len(summary) == 1:
            return self._evaluate_single(summary, reference_summary)
        else:
            return self._evaluate_multi(summary, reference_summary)

    def _evaluate_single(self, summary, reference_summary):
        bert_score_res = self.bertscore.score(summary, reference_summary, lang=self.lang)
        return {
            "bert_score": bert_score_res,
        }

    def _evaluate_multi(self, summary, reference_summary):
        summary = [str(s) for s in summary]
        reference_summary = [str(rs) for rs in reference_summary]
        bert_score_res = self.bertscore.score(summary, reference_summary, lang=self.lang)
        results = [float(bert_score_res[0][0]) for i in range(len(bert_score_res))]
        if self.avg:
            return {
                "bert_score": sum(results) / len(results),
            }
        
        return {
            "bert_score": results,
        }

