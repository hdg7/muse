import os

from pytest import fixture

from muse.data_importer import import_data
from muse.evaluation.classical.rouge_metric import RougeMetric
from muse.summarizer import MT5


@fixture
def document_path():
    return os.path.join(os.path.dirname(__file__), "xlsum")


def test_import_document_source_target(document_path):
    documents = import_data(document_path, "document", "en")
    documents = [doc for doc in documents if doc.text != ""]
    assert isinstance(documents, list)
    assert len(documents) == 100
    mt5sum = MT5({"model_name": "csebuetnlp/mT5_multilingual_XLSum"})
    summary = mt5sum.summarize(documents)
    assert len(summary) == len(documents)
    print(summary[1])
    print(documents[1].summary)
    rouge = RougeMetric({})
    rouge_score = rouge.evaluate(
        summary,
        reference_summary=[doc.summary for doc in documents],
        reference_text=[doc.text for doc in documents],
    )
    assert len(rouge_score["rouge_score"]) == 100
