import time

from snr.interfaces import *


class Timer(TimerProtocol):
    def __init__(self):
        self.start_time = time.time()

    def current_s(self) -> float:
        return time.time() - self.start_time
