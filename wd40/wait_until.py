import time


def wait_until(some_predicate, timeout=5, period=0.25, *args, **kwargs):
    """
    :param some_predicate: must be a callable who return a boolean condition
    :param timeout: timeout
    :param period: time between each check
    :param args: for predicate
    :param kwargs: for predicate
    :return: False on timeout
    """
    must_end = time.time() + timeout
    while time.time() < must_end:
        if some_predicate(*args, **kwargs):
            return True
        time.sleep(period)
    return False
