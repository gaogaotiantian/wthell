import sys
from .wthell import WTHell
from .main import main


__version__ = "0.1.1"

if "wth" not in locals():
    wth = WTHell()
    wth._sys_excepthook = sys.excepthook
    sys.excepthook = wth.excepthook
