from muse.evaluation.evaluation import Evaluation
from muse.utils.plugins import import_from_plugin
from muse.utils.resource_errors import UnknownResourceError


def resolve_evaluator(
    evaluation_metric: str, options: dict[str, any] = None
) -> Evaluation:
    """
    Import an evaluation metric using the plugins.

    :param evaluation_metric: The evaluation metric to import.
    :param options: Options to initialize the evaluation metric.
    :return: The evaluation metric.
    :raises UnknownResourceError: If the evaluation metric is not found.
    """

    evaluations = Evaluation.__subclasses__()
    evaluations.sort(key=lambda x: x.plugin, reverse=True)
    for evaluation in evaluations:
        possible_names = [
            str(evaluation_metric).lower(),
            f"{evaluation_metric}Metric".lower(),
        ]
        if evaluation.__name__.lower() in possible_names:
            return evaluation(options)

    raise UnknownResourceError(evaluation_metric)


def get_available_evaluators() -> list[str]:
    """
    Get all the available evaluation metrics.

    :return: List of available evaluation metrics.
    """

    return [importer.__name__ for importer in Evaluation.__subclasses__()]


def get_evaluators_options() -> list[tuple[str, dict[str, any]]]:
    """
    Get the options for all the available evaluation metrics.

    :return: List of tuples containing the name of the evaluation metric and its options.
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
        for importer in Evaluation.__subclasses__()
    ]


import_from_plugin("evaluations", Evaluation, "evaluation", "evaluator", "evaluators")
