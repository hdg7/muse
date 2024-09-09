"""
MuSE is an evaluation system for summarization engines.

The license for this software is Apache 2.0. Please see the LICENSE file for more information.
"""
import sys

from argparse import Namespace

# Potentially needed
# from nltk import download

# download('punkt')
# download('averaged_perceptron_tagger')
# download('maxent_ne_chunker')
# download('words')
# download('stopwords')
# download('wordnet')
# download('maxent_ne_chunker')
# download('words')
# download('stopwords')
# download('wordnet')
# download('maxent_ne_chunker')

def evaluate_metric(system, data, metrics):
    # This should be moved somewhere universal, so it can be reused in the library
    raise NotImplementedError("Evaluation of metrics not yet implemented")


def main(args: Namespace) -> int:
    try:
        if args.evType == "metrics":
            evaluate_metric(args.system, args.data, args.metrics)
        elif args.evType == "reference":
            raise NotImplementedError("Reference evaluation not yet implemented")
        elif args.evType == "llms":
            raise NotImplementedError("Language model evaluation not yet implemented")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0
