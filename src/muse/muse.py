import data_manager.document
import muse_system.extractive.sumy_connector
import evaluation.classical.rouge_metric
import muse_system
import evaluation

class Muse:
    def __init__(self):
        systems = []
        evMetrics = []
        

    def dataManager(self,datatype,dataPath,dataLanguage):
        if(datatype == "single"):
            self.dataManager = data_manager.document.Document(dataPath,dataLanguage)
#        elif(datatype == "multi"):

    def system(self,systemList):
        if("sumy" in systemList):            
            self.sumy = muse_system.extractive.sumy_connector.Sumy()
            systems.append(self.sumy)
        pass

    def evSummary(self,evMetricsList):
        if("rouge" in evMetricsList):
            self.rouge = evaluation.classical.rouge_metric.Rouge()
            evMetrics.append(self.rouge)
        pass

    def run(self):
        for metric in evMetrics:
            for system in systems:
                print(metric.evaluate(system.run(self.dataManager.data, self.dataManager.reference)))
        
        pass
