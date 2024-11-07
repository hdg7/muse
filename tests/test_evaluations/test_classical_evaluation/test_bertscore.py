from muse.evaluation import BertScoreMetric

def test_bertscore_metric_single():
    bert_score_met = BertScoreMetric({})
    summaries = [
        "This is a long text that needs to be summarized. It is very long and boring. I am trying to "
        "make it shorter. Maybe we can try to write something a little bit longer."
    ]
    reference_summaries = [
        "Something else, everything is different. This is not the same text."
    ]
    result = bert_score_met.evaluate(summaries, reference_summary=summaries)
    assert result["bert_score"][0] == 1.0

    result = bert_score_met.evaluate(summaries, reference_summary=reference_summaries)
    assert result["bert_score"][0] < 0.9





def test_bertscore_metric_multi():
    summaries = [
        "Cars are very useful for transportation. They are very fast and efficient.",
        "Boots are very useful for walking. They are very comfortable and durable.",
    ]
    reference_summaries = [
        "Cars are motor vehicles that are used for transportation. They are fast and efficient.",
        "Boots are shoes that are used for walking. They are comfortable and durable.",
    ]
    bert_score_met = BertScoreMetric({})
    result = bert_score_met.evaluate(summaries, reference_summary=summaries)
    print(result)
    assert result["bert_score"][0]  == 1.0

    result = bert_score_met.evaluate(summaries, reference_summary=reference_summaries)
    assert 0.9 <  result["bert_score"][0] < 1.0



