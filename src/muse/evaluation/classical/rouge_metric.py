# This object is used to calculate the rouge metric for the generated summaries
from rouge import Rouge


class RougeMetric:
    def __init__(self, args=None):
        if args is not None:
            self.args = args
        self.rouge = Rouge()

    def evaluate(self, original, generated):
        self.rouge_score = self.rouge.get_scores(str(original), str(generated))
        return self.rouge_score
