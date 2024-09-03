#This object is used to calculate the blue metric for the generated summaries
from nltk.translate.bleu_score import corpus_bleu
import os
import sys

class BleuMetric:
    def __init__(self, args):
        self.args = args

    def evaluate(self):
        self.bleu_score = corpus_bleu(self.args.data, self.args.system)
        return self.bleu_score    
