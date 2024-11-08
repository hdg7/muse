from muse.evaluation import RougeMetric
import statistics

def test_rouge_metric_single():
    rouge_metric = RougeMetric({})
    summaries = [
        "This is a long text that needs to be summarized. It is very long and boring. I am trying to "
        "make it shorter. Maybe we can try to write something a little bit longer."
    ]
    reference_summaries = [
        "Something else, everything is different. This is not the same text."
    ]
    result = rouge_metric.evaluate(summaries, reference_summary=summaries)
    assert result["rouge_score"][0]["rouge-1"]["r"] == 1.0

    result = rouge_metric.evaluate(summaries, reference_summary=reference_summaries)
    assert result["rouge_score"][0]["rouge-1"]["r"] < 0.5


def test_rouge_metric_multi():
    rouge_metric = RougeMetric({})
    summaries = [
        "Cars are very useful for transportation. They are very fast and efficient.",
        "Boots are very useful for walking. They are very comfortable and durable.",
    ]
    reference_summaries = [
        "Cars are motor vehicles that are used for transportation. They are fast and efficient.",
        "Boots are shoes that are used for walking. They are comfortable and durable.",
    ]
    result = rouge_metric.evaluate(summaries, reference_summary=summaries)
    results = [result["rouge_score"][i]["rouge-1"]["r"] for i in range(len(result["rouge_score"]))]
    assert statistics.mean(results) == 1.0

    result = rouge_metric.evaluate(summaries, reference_summary=reference_summaries)
    results = [result["rouge_score"][i]["rouge-1"]["r"] for i in range(len(result["rouge_score"]))]
    assert 0.6 <  result["rouge_score"][0]["rouge-1"]["r"] < 0.8

