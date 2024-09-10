"""
MuSE is an evaluation system for summarization engines.

The license for this software is Apache 2.0. Please see the LICENSE file for more information.
"""
from argparse import Namespace
from enum import Enum
from typing import TypedDict, cast

# Potentially needed
# from nltk import download

# download('punkt')
# download('averaged_perceptron_tagger')
# download('maxent_ne_chunker')
# download('words')
# download('stopwords')
# download('wordnet')
# download('maxent_ne_chunker')
# download('words')
# download('stopwords')
# download('wordnet')
# download('maxent_ne_chunker')

__all__ = ["System", "DataType", "EvaluationType", "Options", "main"]


class System(Enum):
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
    system: list[System]
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
