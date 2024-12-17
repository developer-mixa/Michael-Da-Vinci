import time

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        execution_time = (end - start)
        return result
    return wrapper