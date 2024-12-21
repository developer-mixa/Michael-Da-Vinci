import functools
import time

from prometheus_client import Histogram


def analyze_execution_time(histogram: Histogram):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            result = func(*args, **kwargs)
            end = time.monotonic()
            histogram.observe(end - start)
            return result

        return wrapper

    return decorator
