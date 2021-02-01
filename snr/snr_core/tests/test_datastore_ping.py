import logging
import time

from snr.snr_core.base import *
from snr.snr_core.utils.test_base import *


class PingTestEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent_node: NodeProtocol,
                 name: str):
        super().__init__(factory,
                         parent_node,
                         name)
        self.log.setLevel(logging.WARN)
        self.                    task_handlers = {
            (TaskType.event, "ping_request"):
            self.store_ping,
            (TaskType.process_data, "ping"):
            self.process_ping
        }
        self.produced_task: bool = False

    def start(self) -> None:
        self.parent.schedule(task.event("ping_request"))

    def store_ping(self, t: Task, key: TaskId) -> SomeTasks:
        self.parent.store_data("ping", time.time())
        self.dbg("Storing ping page")
        return None

    def process_ping(self, t: Task, key: TaskId) -> SomeTasks:
        data = self.parent.get_data("ping")
        if not isinstance(data, float):
            self.err("Stored ping data %s was not a float", data)
            return None
        start: float = data
        self.info("Datastore ping latency: %s ms",
                  (time.time() - float(start)) * 1000)
        return task.terminate("test_endpoint_done")


class PingTestFactory(EndpointFactory):
    def __init__(self):
        super().__init__(None)

    def get(self, parent: NodeProtocol) -> EndpointProtocol:
        return PingTestEndpoint(self,
                                parent,
                                "ping_test_endpoint")


class TestDatastorePing(SNRTestBase):

    def test_dds_ping(self):
        with self.expector({
            (TaskType.event, "ping_request"): 1,
            (TaskType.store_page, "ping"): 1,
            (TaskType.process_data, "ping"): 1,
            TaskType.terminate: 1,
        }) as expector:
            self.run_test_node([
                PingTestFactory(),
                ExpectorEndpointFactory(expector),
            ])


if __name__ == '__main__':
    unittest.main()