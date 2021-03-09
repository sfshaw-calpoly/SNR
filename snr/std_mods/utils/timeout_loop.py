import time

from snr.core import *
from snr.protocol import *
from snr.type_defs import *


class TimeoutLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent_node: NodeProtocol,
                 timeout_s: float,
                 task: Task,
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         "timeout_loop")
        self.timeout_s = timeout_s
        self.task = task

    def setup(self) -> None:
        if self.timeout_s > 0:
            time.sleep(self.timeout_s)
        self.parent.schedule(self.task)
