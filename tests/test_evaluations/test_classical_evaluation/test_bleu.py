from muse.evaluation import BleuMetric


def test_bleu_metric_single():
    bleu_metric = BleuMetric({})
    summaries = [
        "This is a long text that needs to be summarized. It is very long and boring. I am trying to "
        "make it shorter. Maybe we can try to write something a little bit longer."
    ]
    reference_summaries = [
        "Something else, everything is different. This is not the same text."
    ]
    result = bleu_metric.evaluate(summaries, reference_summary=summaries)
    assert result["bleu_score"] == 1.0

    result = bleu_metric.evaluate(summaries, reference_summary=reference_summaries)
    assert result["bleu_score"] < 1e-10


def test_bleu_metric_multi():
    bleu_metric = BleuMetric({})
    summaries = [
        "Cars are very useful for transportation. They are very fast and efficient.",
        "Boots are very useful for walking. They are very comfortable and durable.",
    ]
    reference_summaries = [
        "Cars are motor vehicles that are used for transportation. They are fast and efficient.",
        "Boots are shoes that are used for walking. They are comfortable and durable.",
    ]
    result = bleu_metric.evaluate(summaries, reference_summary=summaries)
    assert result["bleu_score"] == 1.0

    result = bleu_metric.evaluate(summaries, reference_summary=reference_summaries)
    assert 0.4 < result["bleu_score"] < 0.6
