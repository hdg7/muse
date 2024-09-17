from muse.evaluation import MeteorMetric


def test_meteor_metric_single():
    meteor_metric = MeteorMetric({})
    summaries = [
        "This is a long text that needs to be summarized. It is very long and boring. I am trying to "
        "make it shorter. Maybe we can try to write something a little bit longer."
    ]
    reference_summaries = [
        "Something else, everything is different. This is not the same text."
    ]
    result = meteor_metric.evaluate(summaries, reference_summary=summaries)
    assert result["meteor_scores"] == result["meteor"]
    assert 0.9 < result["meteor"] < 1

    result = meteor_metric.evaluate(summaries, reference_summary=reference_summaries)
    assert result["meteor_scores"] == result["meteor"]
    assert 0.2 < result["meteor"] < 0.5


def test_meteor_metric_multi():
    meteor_metric = MeteorMetric({})
    summaries = [
        "Cars are very useful for transportation. They are very fast and efficient.",
        "Boots are very useful for walking. They are very comfortable and durable.",
    ]
    reference_summaries = [
        "Cars are motor vehicles that are used for transportation. They are fast and efficient.",
        "Boots are shoes that are used for walking. They are comfortable and durable.",
    ]
    result = meteor_metric.evaluate(summaries, reference_summary=summaries)
    for score in result["meteor_scores"]:
        assert 0.9 < score < 1
    assert 0.9 < result["meteor"] < 1

    result = meteor_metric.evaluate(summaries, reference_summary=reference_summaries)
    for score in result["meteor_scores"]:
        assert 0.5 < score < 0.8
    assert 0.5 < result["meteor"] < 0.8
