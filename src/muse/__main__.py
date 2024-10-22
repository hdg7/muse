import sys
from argparse import ArgumentParser, Namespace

from .__about__ import __version__
from .muse import DataType, EvaluationType, SummarizerSystem
from .muse import main as entry_point
from .utils.data_fetcher import main as data_fetcher


def validate_arguments(args: Namespace) -> Namespace:
    if args.evType == "metrics" and not args.metrics:
        raise ValueError("The --metrics argument is required for metrics evaluation")
    if args.evType == "llm" and not args.llm:
        raise ValueError("The --llm argument is required for language model evaluation")

    if args.use_cache and not args.output:
        raise ValueError("The --output argument is required when using cached data")

    return args


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description="MuSE is a evaluation system for summarization engines."
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"MuSE version {__version__}",
        help="Show the version number and exit",
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-s",
        "--system",
        action="append",
        choices=[item.value for item in SummarizerSystem],
        help="The summarization system to evaluate",
        required=True,
    )
    required.add_argument(
        "-t",
        "--type",
        choices=[item.value for item in DataType],
        help="The type of the summarization system",
        required=True,
    )
    required.add_argument(
        "-d",
        "--data",
        help="The data to evaluate the summarization system on",
        required=True,
    )
    required.add_argument(
        "-e",
        "--evType",
        action="append",
        choices=[item.value for item in EvaluationType],
        help="The type of evaluation to perform",
        required=True,
    )

    optional = parser.add_argument_group("optional arguments")

    optional.add_argument(
        "-m", "--metrics", action="append", help="The metrics to use for evaluation"
    )
    optional.add_argument("-l", "--language", help="The language of the data")
    optional.add_argument("--llm", help="Large language model to use for evaluation")
    optional.add_argument(
        "-o",
        "--output",
        help="The output folder to write the results to",
    )
    optional.add_argument(
        "-c", "--config", help="The configuration file to use for evaluation"
    )

    run_config = parser.add_argument_group("run configuration")

    run_config.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase output verbosity"
    )
    run_config.add_argument(
        "--use-cache", action="store_true", help="Use cached data for evaluation, must provide an output folder if wish to use this"
    )

    return validate_arguments(parser.parse_args())


def main():
    sys.exit(entry_point(parse_arguments()))


def fetch():
    data_fetcher()


if __name__ == "__main__":
    main()
