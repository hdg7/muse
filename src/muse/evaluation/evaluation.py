from abc import ABC, abstractmethod


class Evaluation(ABC):
    """
    Abstract class for evaluation metrics
    """

    plugin = False

    @abstractmethod
    def __init__(self, params: dict[str, any]):
        """
        Constructor for the Evaluation class
        """
        pass

    @abstractmethod
    def evaluate(
        self,
        summary: list[str],
        reference_text: list[str] | None,
        reference_summary: list[str] | None = None,
    ) -> dict[str, any]:
        """
        Abstract method to evaluate the summary

        One of reference_text or reference_summary must be provided, unless perhaps to only evaluate readability.

        :param summary: The summary to be evaluated
        :param reference_text: The reference text to compare the summary to (optional)
        :param reference_summary: The reference summary to compare the summary to (optional)
        :return: The evaluation results
        """
        pass
