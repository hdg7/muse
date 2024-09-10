import data_manager
import system
import evaluation

class Muse:
    def __init__(self):
        systems = []
        evMetrics = []
        

    def dataManager(datatype,dataPath,dataLanguage):
        if(datatype == "single"):
            this.dataManager = data_manager.document.Document(dataPath,dataLanguage)
#        elif(datatype == "multi"):

    def system(systemList):
        if("gensim" in systemList):            
            this.gensim = system.extractive.gensim_connector.Gensim()
            systems.append(this.gensim)
        pass

    def evSummary(evMetricsList):
        if("rouge" in evMetricsList):
            this.rouge = evaluation.classical.rouge_metric.Rouge()
            evMetrics.append(this.rouge)
        pass

    def run():
        for metric in evMetrics:
            for system in systems:
                print(metric.evaluate(system.run(this.dataManager.data, this.dataManager.reference)))
        
        pass
