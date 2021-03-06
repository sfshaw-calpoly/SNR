import collections
import logging
from typing import Any, Callable, Deque, Dict, Tuple, TypeVar

from snr.interfaces import *
from snr.type_defs import *

from ..core_utils import Consumer, MovingAvgFilter, Timer

SLEEP_TIME_S = 0.00005

ProfilingResult = Tuple[str, float]
ProfileingData = Tuple[int, MovingAvgFilter]

T = TypeVar("T")


class Profiler(Consumer[ProfilingResult], AbstractProfiler):
    def __init__(self, settings: Settings) -> None:
        super().__init__("profiler",
                         self.store_task,
                         SLEEP_TIME_S,
                         )
        self.log.setLevel(logging.WARNING)
        self.settings = settings
        self.time_dict: Dict[str, ProfileingData] = {}
        self.moving_avg_len = settings.PROFILING_AVG_WINDOW_LEN
        self.timer = Timer()

    def time(self,
             name: str,
             handler: Callable[[Any], T],
             *args: Any
             ) -> T:
        timer = Timer()
        result = handler(*args)
        self.store_event(name, timer.current_s())
        return result

    def store_event(self,
                    task_type: str,
                    runtime: float,
                    ) -> None:
        self.put((task_type, runtime))

    def store_task(self,
                   type_and_runtime: Tuple[str, float],
                   ) -> None:
        (task_id, runtime) = type_and_runtime
        self.log.debug("Ran %s task in %s",
                       task_id, self.format_time(runtime))
        data = self.time_dict.get(task_id)
        if not data:
            data = self.init_task_type(task_id)
        data[1].update(runtime)
        self.time_dict[task_id] = (data[0] + 1, data[1])

        self.log.debug("Task %s has average runtime %s",
                       task_id, data[1].avg())

    def init_task_type(self, task_type: str) -> ProfileingData:
        return (0,
                MovingAvgFilter(collections.deque(maxlen=self.moving_avg_len)))

    def dump(self) -> str:

        items = [(data[0], data[1].avg(), k)
                 for k, data in self.time_dict.items()]
        total_time = self.timer.current_s()
        items_with_stats = [(n, avg, (100 * n * avg / total_time), k)
                            for n, avg, k in items]

        lines = ["Times called,\tAvg runtime,\t\tTask/Loop type,"]
        for n, avg_time, percentage, key in sorted(items_with_stats,
                                                   reverse=True):
            lines.append("{:>12d} x\t{} -> {:>7.3f}%:\t{}".format(
                n,
                self.format_time(avg_time),
                percentage,
                key))
        return "\n".join(lines)

    def avg_time(self, key: str, deque: Deque[float]) -> str:
        return self.format_time(float(sum(deque)) / float(len(deque)))

    def format_time(self, time_s: float) -> str:
        if time_s > 1:
            return "{:>7.3f} s".format(time_s)
        if time_s > 0.001:
            return "{:>7.3f} ms".format(time_s * 1000)
        if time_s > 0.000001:
            return "{:>7.3f} us".format(time_s * 1000000)
        if time_s > 0.000000001:
            return "{:>7.3f} ns".format(time_s * 1000000000)
        return "Could not format time"
