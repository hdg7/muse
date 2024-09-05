from .importer import Importer


class URLConnector(Importer):
    """
    Class for importing data from a URL.
    """
    def import_data(self, data_path: str, document_type: str):
        raise NotImplementedError

    def check_data_path(self, data_path: str):
        raise NotImplementedError

