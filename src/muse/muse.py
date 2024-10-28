import json
import os
from argparse import Namespace
from enum import Enum
from typing import TypedDict, Union, cast

from muse.data_importer.resolver import import_data
from muse.data_manager.conversation.conversation import Conversation
from muse.data_manager.document.document import Document
from muse.data_manager.multi_document.multi_document import MultiDocument
from muse.evaluation.evaluation import Evaluation
from muse.evaluation.resolver import get_available_evaluators, resolve_evaluator
from muse.summarizer.resolver import get_available_summarizers, resolve_summarizer
from muse.summarizer.summarizer import Summarizer
from muse.utils.decorators import with_valid_options

__all__ = [
    "SummarizerSystem",
    "EvaluationSystem",
    "DataType",
    "Options",
    "Muse",
    "main",
]


class DataType(Enum):
    SingleDocument = "document"
    MultiDocument = "multi-document"
    Conversation = "conversation"

    def __str__(self) -> str:
        return self.value


def enum_str(self):
    return self.value


SummarizerSystem = Enum(
    "SummarizerSystem", {s: s.lower() for s in get_available_summarizers()}
)
SummarizerSystem.__str__ = enum_str

EvaluationSystem = Enum(
    "EvaluationSystem", {s: s.lower() for s in get_available_evaluators()}
)
EvaluationSystem.__str__ = enum_str


class Options(TypedDict):
    system: list[SummarizerSystem]
    data_type: DataType
    data: str
    metrics: list[EvaluationSystem]
    language: str
    output: str
    config: str
    use_cache: bool


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
        raise ValueError("No metrics specified")

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

    muse = Muse(options)
    muse.set_data(
        options["data_type"],
        options["data"],
        options["language"],
        config["data_importer_options"],
    )
    muse.add_summarizer(
        *[(s, config["summarizer_options"].get(s, {})) for s in options["system"]]
    )
    muse.add_evaluation(
        *[(m, config["evaluation_options"].get(m, {})) for m in options["metrics"]]
    )
    results = muse.run()
    if options["output"]:
        os.makedirs(options["output"], exist_ok=True)
        print(f"Writing results")
        with open(f"{options['output']}/results.json", "w") as f:
            json.dump(results, f)
        print(f"Writing summaries")
        with open(f"{options['output']}/summaries.json", "w") as f:
            json.dump(muse.summaries, f)
        print(f"Writing reference")
        with open(f"{options['output']}/reference.json", "w") as f:
            json.dump([s.summary for s in muse.data if s.summary != ""], f)
        print(results)
    else:
        print(results)


class Muse:
    @with_valid_options(
        use_cache={"type": bool, "default": False, "help": "Use cached summaries"},
        output={
            "type": str,
            "default": None,
            "help": "Output directory to save results, if none, results are printed",
        },
    )
    def __init__(self, options: Options = None):
        self.summarizers: list[Summarizer] = []
        self.evaluations: list[Evaluation] = []
        self.data: (
            Union[list[Document], list[MultiDocument], list[Conversation]] | None
        ) = None

        self.results: dict[str, dict[str, any]] = {}
        self.use_cache = options.get("use_cache", False)
        self.cache_dir = options.get("output", None)
        self.summaries: dict[str, list[str]] = {}

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
                summarizer = SummarizerSystem(summarizer.lower())
            self.summarizers.append(resolve_summarizer(str(summarizer), params))

    def add_evaluation(self, *evaluations: str | tuple[str, dict[str, any]]):
        for evaluation in evaluations:
            if isinstance(evaluation, tuple):
                evaluation, params = evaluation
            else:
                params = {}
            self.evaluations.append(resolve_evaluator(evaluation, params))

    def run(self):
        if self.use_cache:
            file = f"{self.cache_dir}/summaries.json"
            if os.path.isfile(file):
                with open(file, "r") as f:
                    self.summaries = json.load(f)
            else:
                raise FileNotFoundError("No cached summaries found")

        for summarizer in self.summarizers:
            self._evaluate_summarizer(summarizer)

        return self.get_results()

    def _evaluate_summarizer(self, summarizer: Summarizer) -> None:
        if not self.use_cache:
            self.summaries[summarizer.__class__.__name__] = summarizer.summarize(
                self.data
            )

        summary = self.summaries[summarizer.__class__.__name__]

        results = {}
        for evaluation in self.evaluations:
            result = evaluation.evaluate(
                [elem for elem in summary if elem != ""],
                reference_summary=[s.summary for s in self.data if s.summary != ""],
                reference_text=[str(s) for s in self.data if str(s) != ""],
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
            "metrics": [EvaluationSystem(metric) for metric in options.metrics],
            "output": options.output,
            "config": options.config,
            "language": options.language,
            "use_cache": options.use_cache,
        }

    options = cast(Options, options)

    try:
        evaluate_metric(options)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0
