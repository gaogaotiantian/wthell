class Instrument:
    def __init__(self, frame=None):
        if frame:
            self._frame = frame
            self.do_instrument(frame)

    def get_eval(self, s):
        f = self._frame
        try:
            ret = eval(s, f.f_globals, f.f_locals)
            return True, ret
        except Exception as e:
            return False, e

    def do_instrument(self, frame):
        self.add_code_string(frame)

    def add_code_string(self, frame):
        filename = frame.f_code.co_filename
        firstlineno = frame.f_code.co_firstlineno

        with open(filename, "r") as f:
            lst = f.readlines()

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
            if len(line) - len(stripped_line) <= indent:
                break
            end += 1
        for idx in range(start, end):
            if len(lst[idx].strip()) > 0:
                if idx == frame.f_lineno - 1:
                    lst[idx] = "> " + lst[idx]
                else:
                    lst[idx] = "  " + lst[idx]
        self.code_string = "".join(lst[start:end])
