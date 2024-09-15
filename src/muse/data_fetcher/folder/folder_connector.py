import os
import re

from muse.data_fetcher.data_fetcher import DataFetcher, RawData
from muse.utils.resource_errors import ResourceNotFoundError


class FolderConnector(DataFetcher):
    """
    Class for fetching data from files.
    """

    def fetch_data(self, data_path: str) -> RawData:
        if not self.check_data_path(data_path):
            raise ResourceNotFoundError(data_path)

        data = []
        files = os.listdir(data_path)
        for identifier in [
            f for f in files if "summary" not in f and os.path.isfile(f)
        ]:
            identifier_no_extension = identifier.rsplit(".", 1)[0]
            summary = rf"{re.escape(identifier_no_extension)}_summary.*"
            if any([re.match(summary, f) for f in files]):
                summary = os.path.join(data_path, f"{identifier}_summary")
                with open(summary, "r") as file:
                    summary_data = file.read()

            with open(identifier, "r") as file:
                text_data = file.read()

            if "summary_data" in locals():
                data.append(
                    self._create_data(summary, summary_data, identifier, text_data)
                )
            else:
                data.append(self._create_data(None, None, identifier, text_data))

        for identifier in [f for f in files if os.path.isdir(f)]:
            summary = os.path.join(identifier, "summary")
            summary = rf"{re.escape(summary)}.*"
            files_in_identifier = os.listdir(identifier)
            if any([re.match(summary, f) for f in files_in_identifier]):
                summary = os.path.join(identifier, "summary")
                with open(summary, "r") as file:
                    summary_data = file.read()

            text_data = []
            for file in [f for f in files_in_identifier if "summary" not in f]:
                with open(os.path.join(identifier, file), "r") as f:
                    text_data.append(f.read())

            if "summary_data" in locals():
                data.append(
                    self._create_data(summary, summary_data, identifier, *text_data)
                )
            else:
                data.append(self._create_data(None, None, identifier, *text_data))

        return {
            "data": data,
            "metadata": {
                "resource_name": data_path,
                "resource_type": "directory",
                "data_kind": None,
            },
        }

    @staticmethod
    def _create_data(
        summary_identifier: str | None,
        summary_data: str | None,
        text_identifier: str,
        *text_data: str,
    ) -> RawData:
        if summary_data:
            return {
                "data": [
                    *FolderConnector._create_text(text_identifier, *text_data),
                    {
                        "data": summary_data,
                        "metadata": {
                            "resource_name": summary_identifier,
                            "resource_type": summary_identifier.rsplit(".", 1)[1],
                            "data_kind": "summary",
                        },
                    },
                ],
                "metadata": {
                    "resource_name": text_identifier,
                    "resource_type": "subdirectory",
                    "data_kind": None,
                },
            }
        else:
            return {
                "data": FolderConnector._create_text(text_identifier, *text_data),
                "metadata": {
                    "resource_name": text_identifier,
                    "resource_type": "subdirectory",
                    "data_kind": None,
                },
            }

    @staticmethod
    def _create_text(text_identifier: str, *text_data: str) -> list[RawData]:
        text_data_list = []
        for data in text_data:
            text_data_list.append(
                {
                    "data": data,
                    "metadata": {
                        "resource_name": text_identifier,
                        "resource_type": text_identifier.rsplit(".", 1)[1],
                        "data_kind": "text",
                    },
                }
            )

        return text_data_list

    def check_data_path(self, data_path: str) -> bool:
        return os.path.isdir(data_path)
