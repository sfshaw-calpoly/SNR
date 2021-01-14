from snr.endpoint.endpoint import Endpoint
from snr.factory import Factory

from snr.endpoint.thread_endpoint import ThreadEndpoint
from snr.node import Node


class TimeoutEndpoint(ThreadEndpoint):
    def __init__(self,
                 factory: Factory,
                 parent_node: Node,
                 timeout_s: float
                 ) -> None:
        super().__init__(factory,
                         parent_node,
                         "timeout_endpoint")
        self.timeout_s = timeout_s

    def setup(self) -> None:
        self.sleep(self.timeout_s)
        self.parent_node.set_terminate_flag("Timeout")


class TimeoutEndpointFactory(Factory):
    def __init__(self, seconds: float = 0, ms: float = 0):
        super().__init__("Ping test factory")
        self.timeout_s = seconds + (ms / 1000)

    def get(self, parent_node: Node) -> Endpoint:
        return TimeoutEndpoint(self,
                               parent_node,
                               self.timeout_s)