import os
import sys


def setup():
    try:
        import muse
    except ImportError:
        if "MUSE_HOME" in os.environ:
            sys.path.append(os.environ["MUSE_HOME"])
        elif "HOME" in os.environ:
            sys.path.append(os.environ["HOME"] + "/muse")
        else:
            sys.path.append(
                os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
            )
