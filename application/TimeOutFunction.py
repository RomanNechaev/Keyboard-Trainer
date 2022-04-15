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

    def timed_input(self, caption):
        def echo(c):
            sys.stdout.write(c)
            sys.stdout.flush()

        echo(caption)
        result = []
        start = time.monotonic()
        while time.monotonic() - start < self.timeout:
            if msvcrt.kbhit():
                c = msvcrt.getwch()
                if ord(c) == 13:
                    echo("\r\n")
                    break
                result.append(str(c))
                echo(c)

        if result:
            return result
