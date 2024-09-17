from argparse import Namespace
from enum import Enum
from typing import TypedDict, Union, cast

from muse.data_fetcher.resolver import fetch_data
from muse.data_importer.resolver import import_data
from muse.data_manager.conversation.conversation import Conversation
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.evaluation.classical.rouge_metric import RougeMetric
from muse.evaluation.classical.bleu_metric import BleuMetric
from muse.evaluation.classical.meteor_metric import MeteorMetric
from muse.evaluation.evaluation import Evaluation
from muse.summarizer.extractive.sumy_connector import Sumy
from muse.summarizer.summarizer import Summarizer

__all__ = ["SummarizerSystem", "DataType", "EvaluationType", "Options", "Muse"]


class SummarizerSystem(Enum):
    GenSim = "gensim"
    Sumy = "sumy"


class DataType(Enum):
    SingleDocument = "single-document"
    MultiDocument = "multi-document"
    Conversation = "conversation"


class EvaluationType(Enum):
    Metrics = "metrics"
    Reference = "reference"
    LLM = "llm"


class Options(TypedDict):
    system: list[SummarizerSystem]
    data_type: DataType
    data: str
    evaluation_type: list[EvaluationType]
    metrics: list[str]
    llm: list[str]
    output: str
    config: str


def evaluate_metric(options: Options) -> None:
    # This should be moved somewhere universal, so it can be reused in the library
    raise NotImplementedError("Evaluation of metrics not yet implemented")


class Muse:
    def __init__(self):
        self.summarizers: list[Summarizer] = []
        self.evaluations: list[Evaluation] = []
        self.data: (
            Union[list[Document], list[MultiDocument], list[Conversation]] | None
        ) = None

        self.results: dict[str, dict[str, any]] = {}

    def set_data(self, datatype: DataType, data_path: str, data_language: str):
        if not isinstance(datatype, DataType):
            datatype = DataType(datatype)
        match datatype:
            case DataType.SingleDocument:
                raw_data = fetch_data(data_path)
                self.data = import_data(raw_data, "document")
            case DataType.MultiDocument:
                raise NotImplementedError("MultiDocument not yet implemented")
            case DataType.Conversation:
                raise NotImplementedError("Conversation not yet implemented")

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
            result = evaluation.evaluate(summary,
                                         reference_summary=[s.summary for s in self.data],
                                         reference_text=[str(s) for s in self.data]
                                         )
            results[evaluation.__class__.__name__] = result
        self.results[summarizer.__class__.__name__] = results

    def get_results(self) -> dict[str, dict[str, any]]:
        return self.results


def main(options: Options | Namespace) -> int:
    if isinstance(options, Namespace):
        options = {
            "system": options.system,
            "data_type": options.type,
            "data": options.data,
            "evaluation_type": options.evType,
            "metrics": options.metrics,
            "llm": options.llm,
            "output": options.output,
            "config": options.config,
        }

    options = cast(Options, options)

    try:
        if options["evaluation_type"] == EvaluationType.Metrics:
            evaluate_metric(options)
        elif options["evaluation_type"] == EvaluationType.Reference:
            raise NotImplementedError("Reference evaluation not yet implemented")
        elif options["evaluation_type"] == EvaluationType.LLM:
            raise NotImplementedError("Language model evaluation not yet implemented")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0
