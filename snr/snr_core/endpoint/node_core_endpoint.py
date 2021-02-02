from snr.snr_protocol import *
from snr.snr_types import *

from .endpoint import Endpoint
from .endpoint_factory import EndpointFactory

NODE_CORE_NAME_SUFFIX = "_core_endpoint"

TASK_TYPE_LIST_ENDPOINTS = "list_endpoints"


class NodeCoreEndpoint(Endpoint):
    def __init__(self,
                 factory: EndpointFactory,
                 parent: NodeProtocol,
                 ) -> None:
        super().__init__(factory,
                         parent,
                         parent.name + NODE_CORE_NAME_SUFFIX)
        self.task_handlers = {
            TaskType.terminate: self.task_handler_terminate,
            TaskType.store_page: self.task_handler_store_page,
            TaskType.reload: self.task_handler_reload,
        }

    def start(self) -> None:
        pass

    def terminate(self) -> None:
        pass

    def task_source(self) -> SomeTasks:
        return None

    def task_handler_store_page(self, t: Task, key: TaskId) -> SomeTasks:
        page = t.val_list[0]
        if isinstance(page, Page):
            self.parent.synchronous_store(page)
        else:
            self.err("Store page task value was not a page: %s", page)
        return None

    def task_handler_terminate(self, t: Task, key: TaskId) -> SomeTasks:
        # if ("all" in t.val_list
        #         or self.parent_node.name in t.val_list
        #         or "node" in t.val_list):
        self.parent.set_terminate_flag(f"terminate_task:{t.name}")
        return None

    def task_handler_reload(self, t: Task, key: TaskId) -> SomeTasks:
        endpoint_name = t.val_list[0]
        endpoint = self.parent.endpoints.get(endpoint_name)
        if isinstance(endpoint, EndpointProtocol):
            self.info("Reloading endoint: %s", endpoint_name)
            endpoint.reload()
            self.parent.endpoints.pop(endpoint_name)
            new_name = self.parent.add_component(endpoint.factory)
            if new_name:
                self.parent.endpoints[new_name].start()
            else:
                self.warn("Failed to restart reloaded endpoint %s",
                          endpoint_name)
        else:
            self.warn("Endpoint %s not found", endpoint_name)

        return None
