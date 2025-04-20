import time
from functools import wraps
from typing import Any, Callable

from prometheus_client import Histogram


def analyze_execution_time(histogram: Histogram) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.monotonic()
            result = func(*args, **kwargs)
            end = time.monotonic()
            histogram.observe(end - start)
            return result

        return wrapper

    return decorator
