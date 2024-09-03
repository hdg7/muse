# MuSE is a evaluation system for summarization engines. It is a command line tool that takes a set of summaries and a set of reference (or not) summaries and outputs a set of evaluation metrics. The system is designed to be flexible and extensible, allowing for easy addition of new evaluation metrics. The system is also designed to be easy to use, with a simple command line interface and a simple output format.
# The license for this software is Apache 2.0. Please see the LICENSE file for more information.

# Muse accepts the following options in the command line
# -h, --help: Show the help message and exit
# -s, --system: The summarization system to evaluate
# -t, --type: The type of the summarization system (single-document, multi-document, conversation)
# -d, --data: The data to evaluate the summarization system on
# -e, --evType: The type of evaluation to perform (metrics, reference, llms)
# -m, --metrics: The metrics to use for evaluation
# -c, --config: The configuration file to use for evaluation
# -o, --output: The output file to write the results to
# -v, --version: Show the version number and exit
# -l, --language: The language of the data
# --llm: language model to use for evaluation


import argparse
import sys


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

# Function to evaluate metrics


def evaluate_metrics(args):
    if args.system == "rouge":
        evaluate_rouge(args)
    elif args.system == "bleu":
        evaluate_bleu(args)
    elif args.system == "meteor":
        evaluate_meteor(args)
    else:
        print("Invalid summarization system")
        sys.exit(1)


def get_args():
    parser = argparse.ArgumentParser(
        description="MuSE is a evaluation system for summarization engines."
    )
    parser.add_argument(
        "-s", "--system", help="The summarization system to evaluate", required=True
    )
    parser.add_argument(
        "-t",
        "--type",
        help="The type of the summarization system (single-document, multi-document, conversation)",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--data",
        help="The data to evaluate the summarization system on",
        required=True,
    )
    parser.add_argument(
        "-e",
        "--evType",
        help="The type of evaluation to perform (metrics, reference, llms)",
        required=True,
    )
    parser.add_argument("-m", "--metrics", help="The metrics to use for evaluation")
    parser.add_argument(
        "-c", "--config", help="The configuration file to use for evaluation"
    )
    parser.add_argument(
        "-o", "--output", help="The output file to write the results to"
    )
    parser.add_argument("-v", "--version", help="Show the version number and exit")
    parser.add_argument("-l", "--language", help="The language of the data")
    parser.add_argument("--llm", help="language model to use for evaluation")
    return parser.parse_args()


# Main function
def main():
    args = get_args()
    if args.version:
        print("MuSE version 1.0")
        sys.exit(0)
    if args.evType == "metrics":
        evaluate_metrics(args)
    elif args.evType == "reference":
        evaluate_reference(args)
    elif args.evType == "llms":
        evaluate_llms(args)
    else:
        print("Invalid evaluation type")
        sys.exit(1)
