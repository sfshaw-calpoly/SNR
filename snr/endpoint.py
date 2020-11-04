from typing import Any, Dict, List

from snr.context import Context
from snr.factory import Factory
from snr.task import TaskHandler, TaskSource


class Endpoint(Context):
    def __init__(self,
                 parent_node: Any,
                 name: str,
                 task_producers: List[TaskSource] = [],
                 task_handlers: Dict[str, TaskHandler] = {}
                 ) -> None:
        super().__init__(name, parent_node)
        self.parent_node = parent_node
        self.task_producers = task_producers
        self.task_handlers = task_handlers

    def set_terminate_flag(self, reason: str):
        # Stub for synchronous endpoints
        pass

    def terminate(self) -> None:
        self.warn("{} does not implement terminate()",
                  [self.name])
        raise NotImplementedError

    def join(self):
        # Stub for synchronous endpoints
        return

    def __repr__(self) -> str:
        return self.name


class EndpointFactory(Factory):
    def __init__(self):
        pass

    def get(self, parent_node: Any) -> List[Endpoint]:
        return self.get_endpoints(parent_node)

    def get_endpoints(self, parent_node: Any = None) -> List[Endpoint]:
        raise NotImplementedError


"""Example factory that might be implemented for an endpoint
"""
# class FactoryTemplate(Factory):
#     def __init__(self, stuff: str):
#         super().__init__()
#         self.stuff = stuff

#     def get(self
#             ...
#             ) -> List[Endpoint]:
#         return [Endpoint(stuff)]
