import data_manager
import system
import evaluation

class Muse:
    def __init__(self):
        pass

    def dataManager(datatype,dataPath,dataLanguage):
        if(datatype == "single"):
            this.dataManager = data_manager.document.Document(dataPath,dataLanguage)
#        elif(datatype == "multi"):

    def system(systemList):
        if(systemList == "gensim"):
            this.system = system.extractive.gensim_connector.Gensim()
        pass

    def evSummary(evMetricsList):
        pass

    def run():
        pass
