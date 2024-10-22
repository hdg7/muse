from muse.summarizer.summarizer import Summarizer
from muse.utils.plugins import import_from_plugin
from muse.utils.resource_errors import UnknownResourceError


def resolve_summarizer(summarizer: str, options: dict[str, any] = None) -> Summarizer:
    """
    Import summarizer using the plugins.

    :param summarizer: The summarizer to import.
    :param options: Options to initialize the evaluation metric.
    :return: The evaluation metric.
    :raises UnknownResourceError: If the evaluation metric is not found.
    """

    importers = Summarizer.__subclasses__()
    importers.sort(key=lambda x: x.plugin, reverse=True)
    for importer in importers:
        if importer.__name__.lower() == summarizer.lower():
            return importer(options)

    raise UnknownResourceError(summarizer)


def get_available_summarizers() -> list[str]:
    """
    Get all the available summarizers.

    :return: List of available summarizers.
    """

    return [importer.__name__ for importer in Summarizer.__subclasses__()]


import_from_plugin("summarizers", Summarizer, "summarizer", "summarizer", "summarizers")
