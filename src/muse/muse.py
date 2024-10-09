from argparse import Namespace
from enum import Enum
from typing import TypedDict, Union, cast

from muse.data_importer.resolver import import_data
from muse.data_manager.conversation.conversation import Conversation
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.evaluation.classical.bleu_metric import BleuMetric
from muse.evaluation.classical.meteor_metric import MeteorMetric
from muse.evaluation.classical.rouge_metric import RougeMetric
from muse.evaluation.evaluation import Evaluation
from muse.summarizer.abstractive.mT5 import MT5
from muse.summarizer.extractive.sumy_connector import Sumy
from muse.summarizer.summarizer import Summarizer

__all__ = ["SummarizerSystem", "DataType", "EvaluationType", "Options", "Muse", "main"]


class SummarizerSystem(Enum):
    GenSim = "gensim"
    Sumy = "sumy"
    mT5 = "mT5"

    def __str__(self) -> str:
        return self.value


class DataType(Enum):
    SingleDocument = "document"
    MultiDocument = "multi-document"
    Conversation = "conversation"

    def __str__(self) -> str:
        return self.value


class EvaluationType(Enum):
    Metrics = "metrics"
    Reference = "reference"
    LLM = "llm"

    def __str__(self) -> str:
        return self.value


class Options(TypedDict):
    system: list[SummarizerSystem]
    data_type: DataType
    data: str
    evaluation_type: list[EvaluationType]  # May not be needed
    metrics: list[str]
    llm: list[str]
    language: str
    output: str
    config: str


def _parse_config(config: str) -> dict[str, any]:
    if not config:
        return {}

    import json
    import os

    if os.path.isfile(config):
        with open(config, "r") as f:
            return json.load(f)

    return json.loads(config)


def evaluate_metric(options: Options) -> None:
    config = _parse_config(options["config"])

    if not options["metrics"]:
        options["metrics"] = []
    if not options["llm"]:
        options["llm"] = []

    if options["metrics"] == [] and options["llm"] == []:
        raise ValueError("No metrics or llm specified")

    if not options["system"]:
        raise ValueError("No summarizer specified")

    if not options["data"]:
        raise ValueError("No data specified")

    if not options["language"]:
        import warnings

        warnings.warn("No language specified, defaulting to English")
        options["language"] = "en"

    if not options["data_type"]:
        raise ValueError("No data type specified")

    muse = Muse()
    muse.set_data(options["data_type"], options["data"], options["language"], config)
    # TODO: Add support for option passing to summarizer and evaluation too, we will just need to
    #       check the config for names corresponding to the summarizer and evaluation methods selected
    muse.add_summarizer(*options["system"])
    muse.add_evaluation(*options["metrics"], *options["llm"])
    results = muse.run()
    if options["output"]:
        print(results)
    else:
        print(results)


class Muse:
    def __init__(self):
        self.summarizers: list[Summarizer] = []
        self.evaluations: list[Evaluation] = []
        self.data: (
            Union[list[Document], list[MultiDocument], list[Conversation]] | None
        ) = None

        self.results: dict[str, dict[str, any]] = {}

    def set_data(
        self,
        datatype: DataType,
        data_path: str,
        data_language: str,
        options: dict[str, any] = None,
    ):
        if not isinstance(datatype, DataType):
            datatype = DataType(datatype)
        self.data = import_data(data_path, str(datatype), data_language, options)
        if isinstance(self.data, list):
            if isinstance(self.data[0], Document):
                self.data = [doc for doc in self.data if doc.text != ""]

                
    def add_summarizer(
        self, *summarizers: SummarizerSystem | tuple[SummarizerSystem, dict[str, any]]
    ):
        for summarizer in summarizers:
            if isinstance(summarizer, tuple):
                summarizer, params = summarizer
            else:
                params = {}
            if not isinstance(summarizer, SummarizerSystem):
                summarizer = SummarizerSystem(summarizer)
            match summarizer:
                case SummarizerSystem.GenSim:
                    raise NotImplementedError("GenSim not yet implemented")
                case SummarizerSystem.Sumy:
                    self.summarizers.append(Sumy(params))
                case SummarizerSystem.mT5:
                    self.summarizers.append(MT5(params))

    def add_evaluation(self, *evaluations: str | tuple[str, dict[str, any]]):
        for evaluation in evaluations:
            if isinstance(evaluation, tuple):
                evaluation, params = evaluation
            else:
                params = {}
            match evaluation:
                case "rouge":
                    self.evaluations.append(RougeMetric(params))
                case "bleu":
                    self.evaluations.append(BleuMetric(params))
                case "meteor":
                    self.evaluations.append(MeteorMetric(params))

    def run(self):
        for summarizer in self.summarizers:
            self._evaluate_summarizer(summarizer)

        return self.get_results()

    def _evaluate_summarizer(self, summarizer: Summarizer) -> None:
        summary = summarizer.summarize(self.data)
        results = {}
        for evaluation in self.evaluations:
            result = evaluation.evaluate(
                [elem for elem in summary if elem is not ''],
                reference_summary=[s.summary for s in self.data if s.summary is not ''],
                reference_text=[str(s) for s in self.data if str(s) is not ''],
            )
            results[evaluation.__class__.__name__] = result
        self.results[summarizer.__class__.__name__] = results

    def get_results(self) -> dict[str, dict[str, any]]:
        return self.results


def main(options: Options | Namespace) -> int:
    if isinstance(options, Namespace):
        options = {
            "system": [SummarizerSystem(system) for system in options.system],
            "data_type": DataType(options.type),
            "data": options.data,
            "evaluation_type": [EvaluationType(evType) for evType in options.evType],
            "metrics": options.metrics,
            "llm": options.llm,
            "output": options.output,
            "config": options.config,
            "language": options.language,
        }

    options = cast(Options, options)

    try:
        if EvaluationType.Metrics in options["evaluation_type"]:
            evaluate_metric(options)
        elif EvaluationType.Reference in options["evaluation_type"]:
            raise NotImplementedError("Reference evaluation not yet implemented")
        elif EvaluationType.LLM in options["evaluation_type"]:
            raise NotImplementedError("Language model evaluation not yet implemented")
        else:
            raise ValueError("Invalid evaluation type")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0
