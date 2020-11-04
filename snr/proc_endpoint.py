""" SNR framework for scheduling and task management

Node: Task queue driven host for data and endpoints
AsyncEndpoint: Generate and process data for Nodes
Relay: Server data to other nodes
"""
# import signal
from typing import Callable
from multiprocessing import Process

from snr.endpoint import Endpoint
from snr.node import Node

JOIN_TIMEOUT = 0.5


class ProcEndpoint(Endpoint):
    """An Asynchronous (Thread) endpoint for a node

    An AsyncEndpoint is part of a node, and runs in its own thread. An
    endpoint may produce data to be stored in the Node or retreive data from
    the Node. The endpoint has its loop handler function run according to its
    tick_rate (Hz).
    """

    def __init__(self,
                 parent: Node,
                 name: str,
                 setup_handler: Callable[[], None],
                 loop_handler: Callable[[], None],
                 tick_rate_hz: float
                 ) -> None:
        super().__init__(parent, name)
        self.setup = setup_handler
        self.loop_handler = loop_handler
        self.terminate_flag = False
        self.set_delay(tick_rate_hz)
        if parent:
            self.profiler = parent.profiler
        else:
            self.profiler = None

    def set_delay(self, tick_rate_hz: float):
        if tick_rate_hz == 0:
            self.delay = 0.0
        else:
            self.delay = 1.0 / tick_rate_hz

    def start_loop(self):
        self.info("Starting proc endpoint {} process", [self.name])
        self.proc = self.get_proc()
        self.proc.start()

    def get_proc(self):
        return Process(target=self.threaded_method, daemon=False)

    def join(self):
        self.set_terminate_flag("join")
        self.proc.join(JOIN_TIMEOUT)

    def threaded_method(self):
        # signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            self.setup()
            while not self.terminate_flag:

                if self.profiler is None:
                    self.loop_handler()
                else:
                    self.profiler.time(self.name, self.loop_handler)

                    # self.dbg("profiling_endpoint",
                    #       "Ran {} task in {:6.3f} us",
                    #       [self.name, runtime * 1000000])
                self.tick()
        except (Exception, KeyboardInterrupt) as e:
            self.err("{}, e: {}", [self.name, str(e)])
            # self.parent.set_terminate_flag(str(e))

        self.dbg("Proc endpoint {} exited loop",
                 [self.name])
        self.terminate()
        return

    def get_name(self):
        return self.name

    def tick(self):
        if (self.delay == 0.0):
            self.warn("Proc_endpoint {} does not sleep (max tick rate)",
                      [self.name])
        else:
            self.sleep(self.delay)

    def set_terminate_flag(self, reason: str):
        self.terminate_flag = True
        self.info("Preparing to terminate proc_endpoint {} for {}",
                  [self.name, reason])

    def terminate(self) -> None:
        raise NotImplementedError
