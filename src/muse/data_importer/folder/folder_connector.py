from muse.data_importer.data_importer import Importer


class FolderConnector(Importer):
    """
    Class for importing data from a folder.
    """

    def import_data(self, data, document_type):
        raise NotImplementedError

    def check_data(self, data, document_type):
        raise NotImplementedError
