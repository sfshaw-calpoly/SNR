from time import time


class Timer:
    def __init__(self):
        self.start_time = time()

    def current(self) -> float:
        return time() - self.start_time
