"""
Various tools to make life easier.
"""
import logging

log = logging.getLogger('shapiro')


def is_close(a: float, b: float, relative_tolerance: float=1e-09, absolute_tolerance: float=0.0) -> bool:
    """
    Same as ``math.isclose()`` but also works with Python versions before 3.5.
    """
    return abs(a - b) <= max(relative_tolerance * max(abs(a), abs(b)), absolute_tolerance)


def signum(value) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
