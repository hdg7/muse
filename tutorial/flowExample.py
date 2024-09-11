import os
import sys

try:
    home = os.environ["MUSE_HOME"]
except KeyError:
    home = os.path.join(os.path.expanduser("~"), "muse")

sys.path.append(home)

from muse.muse import Muse

# Create a new Muse object

muse = Muse()

# Set the specific type of data, scenario and language
muse.dataManager("single", "./exampleFolder", "en")

# Set the specific type of model or system for the summarization
muse.system(["sumy"])

# Set the specific type of evaluation metrics
muse.evSummary(["rouge", "bleu"])

# Run it
muse.run()
