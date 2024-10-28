from typing import Union

from muse.data_importer.data_importer import Importer
from muse.data_manager.conversation.conversation import Conversation
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.utils.plugins import import_from_plugin
from muse.utils.resource_errors import UnknownResourceError


def import_data(
    data_path: str, document_type: str, language: str, options: dict[str, any] = None
) -> Union[list[Document], list[MultiDocument], list[Conversation]]:
    """
    Import raw data from a given path. we first try to import the data using the plugins, if that fails, we try to import
    the data using the builtin importers.

    :param data_path: Path to the data to be imported.
    :param document_type: Type of document to import, either 'document' or 'multi-document' or 'conversation'.
    :param language: Language of the document.
    :param options: Options to initialize the data importer.
    :return: Raw data.
    """

    importers = Importer.__subclasses__()
    importers.sort(key=lambda x: x.plugin, reverse=True)
    for importer in importers:
        importer = importer(options)
        if importer.check_data(data_path, str(document_type)):
            return importer.import_data(data_path, str(document_type))

    raise UnknownResourceError(data_path)


def get_available_importers() -> list[str]:
    """
    Get all the available importers.

    :return: List of available importers.
    """

    return [importer.__name__ for importer in Importer.__subclasses__()]


def get_importers_options() -> list[tuple[str, dict[str, any]]]:
    """
    Get the options for all the available importers.

    :return: List of tuples containing the name of the importer and its options.
    """

    return [
        (
            importer.__name__,
            (
                importer.__init__.valid_options()
                if hasattr(importer.__init__, "valid_options")
                else {}
            ),
        )
        for importer in Importer.__subclasses__()
    ]


import_from_plugin("importer", Importer, "data_importer", "importers", "data_importers")
