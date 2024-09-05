from .importer import Importer


class FolderConnector(Importer):
    """
    Class for importing data from a folder.
    """
    def import_data(self, data_path: str, document_type: str):
        raise NotImplementedError

    def check_data_path(self, data_path: str):
        raise NotImplementedError
