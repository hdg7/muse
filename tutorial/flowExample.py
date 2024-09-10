

from muse import Muse

# Create a new Muse object

muse = Muse()

#Set the specific type of data, scenario and language
muse.dataManager("single","./exampleFolder", "en")

#Set the specific type of model or system for the summarization
muse.system(["gensim","sumy"])

#Set the specific type of evaluation metrics
muse.evSummary(["rouge","bleu"])

#Run it
muse.run()
    
