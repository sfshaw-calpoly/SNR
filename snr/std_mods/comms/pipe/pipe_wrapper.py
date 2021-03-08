import multiprocessing as mp

from snr.core import *
from snr.type_defs import *


class PipeWrapper(Context, ConnectionProtocol):
    def __init__(self,
                 pipe: mp.connection.Connection,
                 parent: ContextProtocol,
                 ) -> None:
        super().__init__("pipe_wrapper", parent.settings, parent.profiler)
        self.pipe = pipe

    def open(self) -> None:
        pass

    def is_closed(self) -> bool:
        return self.pipe.closed

    def send(self, data: bytes) -> None:
        self.pipe.send(data)

    def poll(self, timeout_s: float) -> bool:
        return self.pipe.poll(timeout_s)

    def recv(self) -> Optional[JsonData]:
        return self.pipe.recv()

    def close(self) -> None:
        self.pipe.close()