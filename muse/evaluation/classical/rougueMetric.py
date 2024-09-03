#This object is used to calculate the rouge metric for the generated summaries
from rouge import Rouge
import os
import sys

class RougeMetric:
    def __init__(self, args):
        self.args = args
        self.rouge = Rouge()

    def evaluate(self):
        self.rouge_score = self.rouge.get_scores(self.args.data, self.args.system)
        return self.rouge_score

    
