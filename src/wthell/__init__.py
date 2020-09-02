import sys
from .wthell import WTHell


__version__ = "0.1.0"

if "wth" not in locals():
    wth = WTHell()
    wth._sys_excepthook = sys.excepthook
    sys.excepthook = wth.excepthook
