from typing import Any, Optional, TextIO

from snr.core import *
from snr.interfaces import *
from snr.type_defs import *


class TextReader(Context):
    def __init__(self,
                 parent: AbstractContext,
                 name: str,
                 filename: str,
                 ) -> None:
        super().__init__(name,
                         parent.settings,
                         parent.profiler,
                         parent.timer)

        self.filename = filename
        self.file: Optional[TextIO] = None

    def open(self) -> None:
        try:
            self.file = open(self.filename)
            self.dbg(f"File {self.filename} opened")
        except Exception as e:
            self.err(f"Error opening file: {e}")
            self.close()

    def read(self) -> Optional[str]:
        if self.file:
            try:
                raw_line = self.file.readline()
                self.dbg(f"Read line: {raw_line}")
                line = raw_line.rstrip()
                if len(line) > 0:
                    return line
            except Exception as e:
                self.err("Error reading file: %s", e)
                return None
        return None

    def close(self) -> None:
        if self.file:
            self.info("Closing file %s", self.filename)
            self.file.close()

    def __enter__(self) -> 'TextReader':
        self.open()
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
