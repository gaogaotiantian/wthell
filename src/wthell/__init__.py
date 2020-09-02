import sys
from .wthell import WTHell


if "wth" not in locals():
    wth = WTHell()
    sys.excepthook = wth.excepthook
    sys.settrace(wth.tracefunc)

__version__ = "0.0.1"
