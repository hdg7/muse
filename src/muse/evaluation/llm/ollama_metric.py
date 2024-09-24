import ollama

from muse.evaluation.evaluation import Evaluation


class OllamaMetric(Evaluation):
    """
    Class to evaluate the OLLAMA metric
    """

    def __init__(self, params):
        faithfulness_model = params.get("faithfulness_model", "qwen2")
        coherence_model = params.get("coherence_model", "qwen2")
        relevance_model = params.get("relevance_model", "qwen2")

        self.faithfulness_model = faithfulness_model
        self.coherence_model = coherence_model
        self.relevance_model = relevance_model

        self.models = [
            faithfulness_model,
            coherence_model,
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

    def _evaluate_faithfulness(self, summary):
        pass

    def _evaluate_coherence(self, summary):
        pass

    def _evaluate_relevance(self, summary):
        pass

    @staticmethod
    def _pull_models(models):
        for model in models:
            ollama.pull(model)

    def _query_model(self, model, text: list[tuple[str, str]]):
        # The text contains a list of messages, where each message is a tuple of the message and the author, e.g.:
        # [
        #     ("System", "You're an llm model to evaluate the summaries"),
        #     ("User", "Evaluate the following summary on the following text: ..."),
        # ]

        pass
