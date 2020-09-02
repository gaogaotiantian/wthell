import traceback
import sys
from .instrument import Instrument
import os
import readline


class WTHell:
    def __init__(self):
        self.frames = []
        self.frame_idx = 0
        self.currentframe = None
        self.exception_frame = None
        self.exception = {}

    def tracefunc(self, frame, event, arg):
        if event == 'call':
            if frame.f_code.co_name == "excepthook":
                sys.settrace(None)
            else:
                self.exception_frame = frame
        return None

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
        self.locate_exception_frame(tb)
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

        if args[0] == "back":
            self.do_back(args[1:])
        elif args[0] == "in":
            self.do_in(args[1:])
        elif args[0] == "clear":
            self.do_clear(args[1:])
        else:
            self.do_eval(cmd)

    def do_back(self, args):
        if self.frame_idx == len(self.frames) - 1:
            print("Already at root, can't go back anymore")
        else:
            self.frame_idx += 1
            self.currentframe = self.frames[self.frame_idx]
            self.show_console()

    def do_in(self, args):
        if self.frame_idx == 0:
            print("Already at stack top, can't go in anymore")
        else:
            self.frame_idx -= 1
            self.currentframe = self.frames[self.frame_idx]
            self.show_console()

    def do_clear(self, args):
        self.show_console()

    def do_eval(self, s):
        success, ret = self.currentframe.get_eval(s)
        print(ret)

    def dbg_console(self):
        self.show_console()
        while True:
            cmd = input(">>> ")
            self.do_cmd(cmd)

    def show_console(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(self.currentframe.code_string)
        print(self.exception["type"], self.exception["value"])
        print()
        self.print_help()

    def print_help(self):
        print("back  -- go to outer frame | in     -- go to inner frame")
        print("clear -- reset the console | ctrl+D -- quit")
        print()
