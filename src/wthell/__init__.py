import sys
from .wthell import WTHell


__version__ = "0.0.3"

if "wth" not in locals():
    wth = WTHell()
    sys.excepthook = wth.excepthook
    sys.settrace(wth.tracefunc)
