from abc import ABC, abstractmethod
from typing import Union

from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument


class Summarizer(ABC):
    """
    Abstract class for summarization algorithms
    """

    def __init__(self, params: dict[str, any]):
        """
        Constructor for the Summarizer class
        """
        pass

    @abstractmethod
    def summarize(self, text: Union[Document, MultiDocument]) -> str:
        """
        Abstract method to summarize the text

        :param text: The text to be summarized
        :return: The summarized text
        """
        pass