from abc import ABC, abstractmethod
from typing import Union

from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument


class Summarizer(ABC):
    """
    Abstract class for summarization algorithms
    """

    plugin = False

    @abstractmethod
    def __init__(self, params: dict[str, any]):
        """
        Constructor for the Summarizer class
        """
        pass

    @abstractmethod
    def summarize(self, texts: Union[list[Document], list[MultiDocument]]) -> list[str]:
        """
        Abstract method to summarize the text

        :param texts: The text to be summarized
        :return: The summarized text
        """
        pass

    @classmethod
    def valid_options(cls):
        """
        Get the valid options for the summarizer

        :return: The valid options for the summarizer
        """
        if not hasattr(cls.__init__, "valid_options"):
            return {}
        return cls.__init__.valid_options()
