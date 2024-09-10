import data_manager.document
import system.extractive.sumy_connector
import evaluation.classical.rouge_metric
import system
import evaluation

from argparse import Namespace
from enum import Enum
from typing import TypedDict, cast


__all__ = ["System", "DataType", "EvaluationType", "Options", "Muse"]


class Muse:
    def __init__(self):
        self.systems = []
        self.evMetrics = []
        

    def dataManager(self,datatype,dataPath,dataLanguage):
        if(datatype == "single"):
            #the datapath is a folder with a  two files, one with the text and the other with the reference
            text = open(dataPath+"/text.txt", "r")
            reference = open(dataPath+"/reference.txt", "r")
            self.dataManager = data_manager.document.Document(text.read(),reference.read())
    def system(self,systemList):
        if("sumy" in systemList):            
            self.sumy = system.extractive.sumy_connector.Sumy(self.dataManager.text)
            self.systems.append(self.sumy)
        pass

    def evSummary(self,evMetricsList):
        if("rouge" in evMetricsList):
            self.rouge = evaluation.classical.rouge_metric.RougeMetric()
            self.evMetrics.append(self.rouge)
        pass

    def run(self):
        for metric in self.evMetrics:
            for model in self.systems:
                print(metric.evaluate(model.summarize(), self.dataManager.summary))



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
