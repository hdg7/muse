import argparse
import os
import sys
from pathlib import Path

from muse.__about__ import __version__
from muse.utils.env import get_cache_dir, get_data_dir

DATASETS = ["seq2seq"]


def validate_arguments(args: argparse.Namespace):
    if args.output:
        try:
            with open(Path(args.output, ".tmp"), "w") as _:
                pass
            os.remove(Path(args.output, ".tmp"))
        except FileNotFoundError as e:
            os.makedirs(args.output, exist_ok=True)
        except PermissionError as e:
            raise ValueError(
                f"Output directory {args.output} is not writable or readable"
            ) from e


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="A data fetcher utility for MuSE. Fetches some example data files."
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"MuSE version {__version__}",
        help="Show the version number and exit",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The directory to output the fetched data to",
        default=get_data_dir(),
    )
    parser.add_argument(
        "-d",
        "--data",
        action="append",
        help="The name of the dataset to fetch",
        choices=DATASETS,
        default=DATASETS,
    )
    parser.add_argument(
        "-k",
        "--keep-intermediate",
        action="store_true",
        help="Keep intermediate files",
    )

    args = parser.parse_args()
    validate_arguments(args)
    return args


def _fetch_seq2seq(output: str, keep_intermediate: bool) -> str:
    import subprocess
    from tempfile import TemporaryDirectory

    import git

    def dependencies(out: str) -> None:
        git.Repo.clone_from("https://github.com/csebuetnlp/xl-sum", out)

        os.chdir(str(Path(out, "seq2seq")))

        try:
            subprocess.run(
                [
                    "conda",
                    "create",
                    "python==3.7.9",
                    "pytorch==1.7.1",
                    "torchvision==0.8.2",
                    "torchaudio==0.7.2",
                    "cudatoolkit=10.2",
                    "-c",
                    "pytorch",
                    "-p",
                    "./env",
                ],
                check=True,
            )
            subprocess.run(["conda", "init", "bash"], check=True)
            subprocess.run(["source", "~/.bashrc"], shell=True, executable="/bin/bash")
            subprocess.run(
                ["conda", "activate", "./env"], shell=True, executable="/bin/bash"
            )
            subprocess.run(["bash", "setup.sh"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                "Failed to run the conda commands. Please check the error message and try again."
            ) from e

    def extraction(extraction_path: str) -> str:
        import tarfile

        import requests

        with TemporaryDirectory() as tmp_dir_:
            file_name = Path(tmp_dir_, "XLSum_complete_v2.0.tar.bz2")
            url = "http://freedevelop.org/muse/XLSum_complete_v2.0.tar.bz2"
            response = requests.get(url)
            with open(file_name, "wb") as f:
                f.write(response.content)

            if not tarfile.is_tarfile(file_name):
                raise ValueError(f"{file_name} is not a valid tar file.")

            with tarfile.open(file_name, mode="r:bz2") as tar:
                tar.extractall(tmp_dir_)
                print(f"Extracted {file_name}")

            os.chdir(output)
            os.makedirs("XLSum_input", exist_ok=True)
            try:
                subprocess.run(
                    [
                        "python3",
                        extraction_path,
                        "-i",
                        str(Path(tmp_dir_, "XLSum_complete_v2.0/")),
                        "-o",
                        "XLSum_input/",
                    ]
                )
                print(f"Extracted data to {output}")
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    "Failed to run the extraction script. Please check the error message and try again."
                ) from e

        return str(Path(output, "XLSum_input"))

    try:
        subprocess.run(["conda", "--version"], check=True)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Conda CLI not found. Please install conda and make sure it is in your PATH."
            "As conda is required to fetch seq2seq dataset."
        )
    try:
        subprocess.run(["wget", "--version"], check=True)
    except FileNotFoundError:
        raise FileNotFoundError(
            "wget not found. Please install wget and make sure it is in your PATH."
            "As wget is required to fetch seq2seq dataset."
        )

    current_cwd = os.getcwd()

    if keep_intermediate:
        dependencies(get_cache_dir())
        result = extraction(str(Path(get_cache_dir(), "seq2seq", "extract_data.py")))
    else:
        with TemporaryDirectory() as tmp_dir:
            dependencies(tmp_dir)
            result = extraction(str(Path(tmp_dir, "seq2seq", "extract_data.py")))

    os.chdir(current_cwd)

    return result


def fetch_data(
    data: str, output: str = get_data_dir(), keep_intermediate: bool = False
) -> str:
    """
    Fetches the data for the given dataset.

    :param data: The name of the dataset to fetch, currently only "seq2seq" is supported.
    :param output: The directory to output the fetched data to. This defaults to the MUSE_DATA environment variable. or ~/.muse/data
    :param keep_intermediate: Whether to keep intermediate files or not. If true, this will be in the MUSE_CACHE directory or ~/.muse/cache
    :return: The path to the fetched data.
    """

    if data == "seq2seq":
        return _fetch_seq2seq(output, keep_intermediate)
    else:
        raise ValueError(f"Unknown dataset {data}")


def fetch_datasets(
    datasets: list[str], output: str = get_data_dir(), keep_intermediate: bool = False
) -> dict[str, str]:
    """
    Fetches the data for the given datasets.

    :param datasets: The names of the datasets to fetch, currently only "seq2seq" is supported.
    :param output: The directory to output the fetched data to. This defaults to the MUSE_DATA environment variable. or ~/.muse/data
    :param keep_intermediate: Whether to keep intermediate files or not. If true, this will be in the MUSE_CACHE directory or ~/.muse/cache
    :return: The paths to the fetched data.
    """
    return {data: fetch_data(data, output, keep_intermediate) for data in datasets}


def main():
    args = parse_arguments()
    paths = []
    errors = []
    for data in args.data:
        try:
            paths.append((data, fetch_data(data, args.output, args.keep_intermediate)))
            print(".", end="")
        except Exception as e:
            print("F", end="")
            errors.append((data, e))

    print()
    print("Fetched data:")
    for data, path in paths:
        print(f"{data}: {path}")

    if args.keep_intermediate:
        print("Intermediate files were kept.")
        print(f"You can find them in {get_cache_dir()}")

    if errors:
        print("Errors:")
        for data, e in errors:
            print(f"{data}: {e}")
            print("  ", end="")
            print("\n  ".join(str(e.__traceback__).split("\n")))

        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
