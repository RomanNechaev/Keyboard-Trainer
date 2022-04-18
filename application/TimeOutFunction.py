import signal
import time
import sys
import msvcrt
from contextlib import contextmanager


class TimeoutFunction:
    def __init__(self, timeout):
        self.timeout = timeout

    @staticmethod
    @contextmanager
    def timeout(self, times):
        signal.signal(signal.SIGALRM, self.raise_timeout)

        signal.alarm(times)

        try:
            yield
        except TimeoutError:
            pass
        finally:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)

    def raise_timeout(self, signum, frame):
        raise TimeoutError
