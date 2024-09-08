from abc import ABC, abstractmethod

from typing import Union

from ..data_manager import Document, MultiDocument


class Summarizer(ABC):
    """
    Abstract class for summarization algorithms
    """

    def __init__(self, text: Union[Document, MultiDocument]):
        """
        Constructor for the Summarizer class
        :param text: The text to be summarized
        """
        self.text = text

    @abstractmethod
    def summarize(self) -> str:
        """
        Abstract method to summarize the text
        :return: The summarized text
        """
        pass
