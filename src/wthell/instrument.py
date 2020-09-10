import os

class Instrument:
    def __init__(self, frame=None, p=print):
        if frame:
            self._frame = frame
            self.do_instrument(frame)
            self.print = p

    def get_eval(self, s):
        f = self._frame
        try:
            ret = eval(s, f.f_globals, f.f_locals)
            return True, ret
        except Exception as e:
            return False, e

    def do_instrument(self, frame):
        self.add_code_string(frame)

    def get_func_code_list(self, filename, firstlineno):
        try:
            with open(filename, "r") as f:
                lst = f.readlines()
        except NotADirectoryError:
            return None, None

        indent = -1
        start = firstlineno
        while start > 0:
            line = lst[start]
            stripped_line = line.lstrip()
            if stripped_line.startswith("def "):
                indent = len(line) - len(stripped_line)
                break
            start -= 1

        end = firstlineno
        while end < len(lst):
            line = lst[end]
            stripped_line = line.lstrip()
            if len(line) - len(stripped_line) <= indent and \
                    not stripped_line.startswith("#"):
                break
            end += 1

        return lst[start:end], start

    def add_code_string(self, frame):
        filename = frame.f_code.co_filename
        firstlineno = frame.f_code.co_firstlineno

        code_list, start = self.get_func_code_list(filename, firstlineno)
        if not code_list:
            self.code_string = "Source file not available"
            return

        for idx in range(0, len(code_list)):
            if len(code_list[idx].strip()) > 0:
                if idx == frame.f_lineno - start - 1:
                    code_list[idx] = "> " + code_list[idx]
                else:
                    code_list[idx] = "  " + code_list[idx]
        self.code_string = "".join(code_list)

    def show_function(self, func_name):
        frame = self._frame
        if func_name in frame.f_locals:
            func = frame.f_locals[func_name]
        elif func_name in frame.f_globals:
            func = frame.f_globals[func_name]
        else:
            self.print("Function {} does not exist".format(func_name))
            return

        if not hasattr(func, "__code__"):
            self.print("Function {} does not exist".format(func_name))

        code = func.__code__
        filename = code.co_filename
        firstlino = code.co_firstlineno

        code_list, _ = self.get_func_code_list(filename, firstlino)

        self.print("".join(code_list))
        self.print("")

    def get_file_path(self):
        frame = self._frame
        filename = frame.f_code.co_filename
        firstlineno = frame.f_code.co_firstlineno
        return "{}({})".format(os.path.abspath(filename), firstlineno)
