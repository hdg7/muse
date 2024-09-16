import os
import sys
from pathlib import Path

# This is here to ensure you can access the muse library, incase it is not installed on your system.
try:
    from muse import Muse
except ImportError:
    home = os.path.abspath(os.path.join(Path.cwd(), "..", "src"))
    sys.path.append(home)

from muse import Muse

# Create a new Muse object
muse = Muse()

# Set the specific type of data, scenario and language
muse.set_data("single-document", os.path.abspath(os.path.join(Path.cwd(), "examples")), "en")

# Set the specific type of model or system for the summarization
muse.add_summarizer("sumy")

# Set the specific type of evaluation metrics
muse.add_evaluation("rouge", "bleu")

# Run it
muse.run()