# This object is used to calculate the meteor metric for the generated summaries
from nltk.translate.meteor_score import meteor_score
import os
import sys


class MeteorMetric:
    def __init__(self, args):
        self.args = args

    def evaluate(self):
        self.meteor_score = meteor_score(self.args.data, self.args.system)
        return self.meteor_score
