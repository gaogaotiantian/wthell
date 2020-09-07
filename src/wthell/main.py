import sys
import os
import argparse
import subprocess
import runpy
from .wthell import WTHell


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs=argparse.REMAINDER)
    parser.add_argument("--module", "-m", nargs="?", default=None)
    options = parser.parse_args(sys.argv[1:])

    if options.command:
        command = options.command
    else:
        print("You need to specify python commands")
        exit(1)
    
    if options.module:
        code = "run_module(modname, run_name='__main__')"
        global_dict = {
            "run_module": runpy.run_module,
            "modname": options.module
        }
        sys.argv = [options.module] + command[:]
    else:
        file_name = command[0]
        if not os.path.exists(file_name):
            if sys.platform in ["linux", "linux2", "darwin"]:
                p = subprocess.Popen(["which", file_name], stdout=subprocess.PIPE)
                file_name = p.communicate()[0].decode("utf-8").strip()
                if not file_name or not os.path.exists(file_name):
                    print("No such file as {}".format(file_name))
                    exit(1)
            else:
                print("No such file as {}".format(file_name))
                exit(1)

        code_string = open(file_name).read()
        global_dict = {
            "__name__": "__main__",
            "__file__": file_name,
            "__package__": None,
            "__cached__": None
        }
        code = compile(code_string, file_name, "exec")
        sys.path.insert(0, os.path.dirname(file_name))
        sys.argv = command[:]
    
    wth = WTHell()
    wth._sys_excepthook = sys.excepthook
    sys.excepthook = wth.excepthook
    global_dict["wth"] = wth
    exec(code, global_dict)