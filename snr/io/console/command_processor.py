from typing import Callable, Dict, List

from snr_core import task
from snr_core.endpoint.synchronous_endpoint import SynchronousEndpoint
from snr_core.endpoint.factory import Factory
from snr_core.node import Node
from snr_core.task import SomeTasks, Task, TaskType

Command = Callable[[List[str]], SomeTasks]


class CommandProcessor(SynchronousEndpoint):
    def __init__(self,
                 factory: Factory,
                 parent: Node
                 ) -> None:
        super().__init__(factory,
                         parent,
                         "console_server",
                         task_handlers={
                             (TaskType.process_data, "console_cmd"):
                             self.process_command})
        self.commands: Dict[str, Command] = {
            "exit": self.cmd_exit,
            "task": self.cmd_schedule_task,
            "reload": self.cmd_reload,
            "list": self.cmd_list,
        }

    def process_command(self, cmd_task: Task) -> SomeTasks:
        args: List[str] = cmd_task.val_list
        self.dbg("Processing command: {}", [str(args)])
        if args:
            command = self.commands.get(args[0])
            if command:
                result: SomeTasks = command(args[1:])
                return result

    def cmd_schedule_task(self, args: List[str]) -> Task:
        type = TaskType(args[0])
        return Task(type, args[1], val_list=args[1:])

    def cmd_exit(self, args: List[str]) -> Task:
        self.dbg("Executing exit command")
        return task.terminate("terminate_cmd")

    def cmd_reload(self, args: List[str]):
        if len(args) == 1:
            return task.reload(args[1])
        else:
            self.warn("Invalid reload args: {}", [args])
            self.debugger.flush()

    def cmd_list(self, args: List[str]) -> SomeTasks:
        options = {
            "endpoints": task.event("cmd_list_endpoints")
        }
        return options.get(args[0])