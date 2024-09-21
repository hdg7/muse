import ollama

from muse.evaluation.evaluation import Evaluation


class OllamaMetric(Evaluation):
    """
    Class to evaluate the OLLAMA metric
    """

    def __init__(self, params):
        readability_model = params.get("readability_model", "qwen2")
        factuality_model = params.get("factuality_model", "qwen2")
        coverage_model = params.get("coverage_model", "qwen2")
        coherence_model = params.get("coherence_model", "qwen2")
        consistency_model = params.get("consistency_model", "qwen2")
        relevance_model = params.get("relevance_model", "qwen2")

        self.readability_weight = params.get("readability_weight", 1)
        self.factuality_weight = params.get("factuality_weight", 1)
        self.coverage_weight = params.get("coverage_weight", 1)
        self.coherence_weight = params.get("coherence_weight", 1)
        self.consistency_weight = params.get("consistency_weight", 1)
        self.relevance_weight = params.get("relevance_weight", 1)

        self.models = [
            readability_model,
            factuality_model,
            coverage_model,
            coherence_model,
            consistency_model,
            relevance_model,
        ]

        self._pull_models(self.models)

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

        if not summary:
            raise ValueError("The summary should not be empty")

        if summary and (
            len(summary) != len(reference_summary)
            or len(summary) != len(reference_text)
        ):
            raise ValueError(
                "The number of summaries and reference summaries should be the same"
            )

        return self._evaluate_multi(summary, reference_text, reference_summary)

    def _evaluate_single(self, summary, reference_text, reference_summary):
        pass

    def _evaluate_multi(self, summary, reference_text, reference_summary):
        pass

    def _evaluate_readability(self, summary):
        pass

    def _evaluate_factuality(self, summary):
        pass

    def _evaluate_coverage(self, summary):
        pass

    def _evaluate_coherence(self, summary):
        pass

    def _evaluate_consistency(self, summary):
        pass

    def _evaluate_relevance(self, summary):
        pass

    @staticmethod
    def _pull_models(models):
        for model in models:
            ollama.pull(model)
