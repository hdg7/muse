import sys
from argparse import ArgumentParser as SuperArgParser
from argparse import Namespace

from .__about__ import __version__
from .data_importer.resolver import get_importers_options
from .evaluation.resolver import get_evaluators_options
from .muse import DataType, EvaluationSystem, SummarizerSystem
from .muse import main as entry_point
from .summarizer.resolver import get_summarizers_options
from .utils.data_fetcher import main as data_fetcher


def validate_arguments(args: Namespace) -> Namespace:
    if args.use_cache and not args.output:
        raise ValueError("The --output argument is required when using cached data")

    return args


class ArgumentParser(SuperArgParser):
    def format_help(self):
        help_message = super().format_help()
        extra_info = (
            "\nConfig:\n"
            "\tThe configuration file should be a JSON file, or JSON string with the following structure:\n"
            "\tIt provides the options for the data importer, summarizer, and evaluation system.\n"
            "\tThe following is the options available for the configuration:\n"
            "\t\tData Importer:\n"
            f"{format_options(get_importers_options())}"
            "\t\tSummarizer:\n"
            f"{format_options(get_summarizers_options())}"
            "\t\tEvaluation System:\n"
            f"{format_options(get_evaluators_options())}"
        )

        return help_message + extra_info


def format_options(options):
    def escape(text):
        return (
            text.replace("\\", "\\\\")
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            .replace("\r\n", "\\r\\n")
        )

    options_str = ""
    for option in options:
        if option[1] == {}:
            options_str += f"\t\t\t{option[0]}: No options available\n"
        else:
            options_str += f"\t\t\t{option[0]}:\n"
            for key, value in option[1].items():
                options_str += f"\t\t\t\t{key} ({value['type'].__name__}) [Default: {escape(str(value['default']))}]: {value['help']}\n"
    return options_str


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
        "-m",
        "--metrics",
        action="append",
        help="The metrics to use for evaluation",
        choices=[item.value for item in EvaluationSystem],
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument("-l", "--language", help="The language of the data")
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
        "--use-cache",
        action="store_true",
        help="Use cached data for evaluation, must provide an output folder if wish to use this",
    )

    return validate_arguments(parser.parse_args())


def main():
    sys.exit(entry_point(parse_arguments()))


def fetch():
    data_fetcher()


if __name__ == "__main__":
    main()
