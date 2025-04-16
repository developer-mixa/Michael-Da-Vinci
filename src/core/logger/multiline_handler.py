import logging
from textwrap import wrap

class MultiLineHandler(logging.StreamHandler):
    def __init__(self, line_length=80):
        super().__init__()
        self.line_length = line_length

    def emit(self, record):
        msg = self.format(record)
        lines = wrap(msg, self.line_length)
        for line in lines:
            self.stream.write(line + '\n')