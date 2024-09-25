import json

from muse.data_importer.data_importer import Importer


class JSONConnector(Importer):
    """
    JSONConnector is a class that imports data from a JSON file.

    It can also be used to import subdata, i.e. data stored as json within other structures such as CSV files.
    """
    def __init__(self, options: dict[str, any] = None):
        pass

    def import_data(self, data_path, document_type):
        pass

    def check_data(self, data_path, document_type):
        try:
            with open(data_path, "r") as file:
                json.load(file)
            return True
        except json.JSONDecodeError:
            return False