import os
import shutil
import tarfile
import tempfile
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import git
import requests

from muse.utils.env import get_data_dir

TMP_DIR = Path(tempfile.gettempdir())
ONE_DAY_AGO = datetime.now() - timedelta(days=1)


def handle_uri(uri: str) -> str:
    """
    Handles the URI and returns the path to the file or folder.
    Also extracts the file if it is a zip or tar file.

    :param uri: URI of the file or folder.
    :return: Path to the file or folder.
    """
    parsed_uri = urlparse(uri)

    scheme = parsed_uri.scheme

    if uri.startswith("git@") or uri.endswith(".git"):
        scheme = "git"

    if scheme == "http" or scheme == "https":
        return extract(download(uri))
    elif scheme == "git":
        return clone(uri)
    elif os.path.exists(uri):
        return extract(uri)
    elif os.path.exists(Path(get_data_dir(), uri)):
        return extract(str(Path(get_data_dir(), uri)))
    else:
        raise FileNotFoundError(f"File or folder not found at {uri}")


def download(uri: str) -> str:
    """
    Downloads the file or folder from the given URI.

    :param uri: URI of the file or folder.
    :return: Path to the downloaded file or folder.
    """
    response = requests.get(uri)
    file_path = TMP_DIR / Path(uri).name
    with open(file_path, "wb") as f:
        f.write(response.content)
    return str(file_path)


def clone(uri: str) -> str:
    """
    Clones the git repository from the given URI. If the repository exists and
    is older than 1 day, it will be deleted and cloned again.

    :param uri: URI of the git repository.
    :return: Path to the cloned repository.
    """
    repo_dir = TMP_DIR / Path(uri).stem

    if repo_dir.exists():
        repo_age = datetime.fromtimestamp(repo_dir.stat().st_mtime)
        if repo_age < ONE_DAY_AGO:
            print(
                f"Repository is older than 1 day. Removing {repo_dir} and re-cloning."
            )
            shutil.rmtree(repo_dir)  # Remove the old repository
        else:
            print(f"Repository is up to date. No need to clone.")
            return str(repo_dir)

    git.Repo.clone_from(uri, repo_dir)
    return str(repo_dir)


def extract(file_path: str) -> str:
    """
    Extracts the zip or tar file, if it is a zip or tar file.

    :param file_path: Path to the zip or tar file.
    :return: Path to the extracted folder.
    """
    if os.path.isdir(file_path):
        return file_path

    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            extracted_folder = TMP_DIR / Path(file_path).stem
            zip_ref.extractall(extracted_folder)
            return str(extracted_folder)
    elif tarfile.is_tarfile(file_path):
        with tarfile.open(file_path, "r") as tar_ref:
            extracted_folder = TMP_DIR / Path(file_path).stem
            tar_ref.extractall(extracted_folder)
            return str(extracted_folder)
    else:
        return file_path


def get_resource_type(path: str) -> str:
    """
    Returns the type of the resource at the given path.

    :param path: Path to the resource.
    :return: Type of the resource.
    """
    if os.path.isdir(path):
        return "directory"

    file_extension = path.rsplit(".", 1)[-1].lower()
    if file_extension is None:
        return "file"
    else:
        return file_extension
