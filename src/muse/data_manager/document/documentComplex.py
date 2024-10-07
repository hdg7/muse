from . import Document

class DocumentComplex:
    def __init__(
        self, pathDocs: str, pathSummaries: str | None = None, metadata: dict | None = None
    ):
        self.documents = []
        self.metadata = metadata
        self.pathDocs = pathDocs
        self.pathSummaries = pathSummaries
        #Upload documents
        self.uploadDocuments()

    def uploadDocuments(self):
        #Read each summary and document from the pathSummaries and pathDocs respectively, each line is a document and summary
        with open(self.pathDocs, "r") as f:
            docs = f.readlines()
        if self.pathSummaries:
            with open(self.pathSummaries, "r") as f:
                summaries = f.readlines()
        else:
            summaries = [None] * len(docs)
        #Create a Document object for each document and summary
        for doc, summary in zip(docs, summaries):
            self.documents.append(Document(doc, summary))

    def getDocuments(self):
        return self.documents

    
