"""
Common structures and function used by multiple modules.
"""
from enum import Enum


class Rating(Enum):
    VERY_BAD = -3
    BAD = -2
    SOMEWHAT_BAD = -1
    UNKNOWN = 0
    SOMEWHAT_GOOD = 1
    GOOD = 2
    VERY_GOOD = 3


# FIXME: Remove this and make all functions using it able to work with a dynamic topic system.
class RestaurantTopic(Enum):
    GENERAL, FOOD, HYGIENE, SERVICE, VALUE = range(5)