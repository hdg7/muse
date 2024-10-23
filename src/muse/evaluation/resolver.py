from muse.evaluation.evaluation import Evaluation
from muse.utils.plugins import import_from_plugin
from muse.utils.resource_errors import UnknownResourceError


def resolve_evaluator(evaluation: str, options: dict[str, any] = None) -> Evaluation:
    """
    Import an evaluation metric using the plugins.

    :param evaluation: The evaluation metric to import.
    :param options: Options to initialize the evaluation metric.
    :return: The evaluation metric.
    :raises UnknownResourceError: If the evaluation metric is not found.
    """

    importers = Evaluation.__subclasses__()
    importers.sort(key=lambda x: x.plugin, reverse=True)
    for importer in importers:
        possible_names = [evaluation.lower(), f"{evaluation}Metric".lower()]
        if importer.__name__.lower() in possible_names:
            return importer(options)

    raise UnknownResourceError(evaluation)


def get_available_evaluators() -> list[str]:
    """
    Get all the available evaluation metrics.

    :return: List of available evaluation metrics.
    """

    return [importer.__name__ for importer in Evaluation.__subclasses__()]


import_from_plugin("evaluations", Evaluation, "evaluation", "evaluator", "evaluators")
