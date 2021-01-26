from snr_core import task
from snr_core.loop.loop_base import LoopBase
from snr_core.loop.loop_factory import LoopFactory
from snr_core.loop.thread_loop import ThreadLoop
from snr_core.node import Node
from snr_core.utils.utils import no_op


class TimeoutLoop(ThreadLoop):
    def __init__(self,
                 factory: LoopFactory,
                 parent_node: Node,
                 timeout_s: float
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         "timeout_loop",
                         no_op,
                         setup=self.setup)
        self.timeout_s = timeout_s

    def setup(self) -> None:
        self.sleep(self.timeout_s)
        self.parent_node.schedule(task.terminate("Timeout"))


class TimeoutLoopFactory(LoopFactory):
    def __init__(self, seconds: float = 0, ms: float = 0):
        super().__init__("Timeout loop factory")
        self.timeout_s = seconds + (ms / 1000)

    def get(self, parent: Node) -> LoopBase:
        return TimeoutLoop(self,
                           parent,
                           self.timeout_s)