from muse.summarizer.summarizer import Summarizer
from muse.utils.plugins import import_from_plugin
from muse.utils.resource_errors import UnknownResourceError


def resolve_summarizer(
    summarizer_system: str, options: dict[str, any] = None
) -> Summarizer:
    """
    Import summarizer using the plugins.

    :param summarizer_system: The summarizer to import.
    :param options: Options to initialize the evaluation metric.
    :return: The summarizer.
    :raises UnknownResourceError: If the evaluation metric is not found.
    """

    summarizers = Summarizer.__subclasses__()
    summarizers.sort(key=lambda x: x.plugin, reverse=True)
    for summarizer in summarizers:
        if summarizer.__name__.lower() == str(summarizer_system).lower():
            return summarizer(options)

    raise UnknownResourceError(summarizer_system)


def get_available_summarizers() -> list[str]:
    """
    Get all the available summarizers.

    :return: List of available summarizers.
    """

    return [importer.__name__ for importer in Summarizer.__subclasses__()]


def get_summarizers_options() -> list[tuple[str, dict[str, any]]]:
    """
    Get the options for all the available summarizers.

    :return: List of tuples containing the name of the summarizer and its options.
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
        for importer in Summarizer.__subclasses__()
    ]


import_from_plugin("summarizers", Summarizer, "summarizer", "summarizer", "summarizers")
