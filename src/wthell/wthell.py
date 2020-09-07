import traceback
import sys
from .instrument import Instrument
import os
import readline
from rich.console import Console
from rich.syntax import Syntax


class WTHell:
    def __init__(self):
        self.frames = []
        self.frame_idx = 0
        self.currentframe = None
        self.exception_frame = None
        self.exception = {}
        self._sys_excepthook = None
        self.console = Console()

    def frame_depth(self, frame):
        f = frame
        ret = 1
        while f.f_back:
            f = f.f_back
            ret += 1
        return ret

    def locate_exception_frame(self, tb):
        # Based on the stack depth on traceback, locate
        # the correct frame of exception
        stack_depth = len(traceback.extract_tb(tb))
        back_depth = self.frame_depth(self.exception_frame) - stack_depth
        for _ in range(back_depth):
            self.exception_frame = self.exception_frame.f_back

    def excepthook(self, type, value, tb):
        self.exception["type"] = type
        self.exception["value"] = value
        self.exception["tb"] = tb
        inner_tb = self.exception["tb"]
        while inner_tb.tb_next:
            inner_tb = inner_tb.tb_next
        self.exception_frame = inner_tb.tb_frame
        self.prepare_data()
        self.dbg_console()

    def __call__(self):
        sys.excepthook = self._sys_excepthook
        self.exception_frame = sys._getframe().f_back
        self.prepare_data()
        self.dbg_console()

    def prepare_data(self):
        self.currentframe = self.exception_frame
        self.frames = []
        while True:
            self.frames.append(Instrument(self.currentframe))
            if self.currentframe.f_back:
                self.currentframe = self.currentframe.f_back
            else:
                break
        self.currentframe = self.frames[0]
        self.frame_idx = 0

    def do_cmd(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return

        args = cmd.split()

        if args[0] == "up" or args[0] == "u":
            self.do_up(args[1:])
        elif args[0] == "down" or args[0] == "d":
            self.do_down(args[1:])
        elif args[0] == "clear" or args[0] == "cl":
            self.do_clear(args[1:])
        elif args[0] == "reset" or args[0] == "r":
            self.do_reset(args[1:])
        elif args[0] == "continue" or args[0] == "c":
            sys.excepthook = self.excepthook
            return False
        else:
            self.do_eval(cmd)
        
        return True

    def do_up(self, args):
        if self.frame_idx == len(self.frames) - 1:
            self.console.print("Already at root, can't go up anymore")
        else:
            self.frame_idx += 1
            self.currentframe = self.frames[self.frame_idx]
            self.show_console()

    def do_down(self, args):
        if self.frame_idx == 0:
            self.console.print("Already at stack top, can't go down anymore")
        else:
            self.frame_idx -= 1
            self.currentframe = self.frames[self.frame_idx]
            self.show_console()

    def do_clear(self, args):
        self.show_console()

    def do_reset(self, args):
        self.frame_idx = 0
        self.currentframe = self.frames[self.frame_idx]
        self.show_console()

    def do_eval(self, s):
        success, ret = self.currentframe.get_eval(s)
        self.console.print(ret)

    def dbg_console(self):
        self.show_console()
        while True:
            try:
                cmd = input(">>> ")
                if not self.do_cmd(cmd):
                    break
            except EOFError:
                exit(0)

    def show_console(self):
        console = self.console
        os.system("cls" if os.name == "nt" else "clear")
        syntax = Syntax(self.currentframe.code_string, "python", theme = "monokai")
        console.print(syntax)
        console.print()
        if self.exception:
            console.print("Exception raised: ", self.exception["type"], self.exception["value"])
        console.print()
        self.print_help()

    def print_help(self):
        console = self.console
        console.print("up(u)       -- go to outer frame  | down(d)  -- go to inner frame")
        console.print("clear(cl)   -- clear the console  | reset(r) -- back to trigger frame")
        console.print("continue(c) -- resume the program | ctrl+D   -- quit")
        console.print()
