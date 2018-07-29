"""
Common structures and function used by multiple modules.
"""
from enum import Enum


class Rating(Enum):
    VERY_BAD = -3
    BAD = -2
    SOMEWHAT_BAD = -1
    SOMEWHAT_GOOD = 1
    GOOD = 2
    VERY_GOOD = 3


# FIXME: Remove this and make all functions using it able to work with a dynamic topic system.
class RestaurantTopic(Enum):
    GENERAL, FOOD, HYGIENE, SERVICE, VALUE = range(5)


_MIN_RATING_VALUE = Rating.VERY_BAD.value
_MAX_RATING_VALUE = Rating.VERY_GOOD.value

RATING_TO_NEGATED_RATING_MAP = {
    Rating.VERY_BAD     : Rating.SOMEWHAT_GOOD,
    Rating.BAD          : Rating.GOOD,
    Rating.SOMEWHAT_BAD : Rating.GOOD,  # hypothetical?
    Rating.SOMEWHAT_GOOD: Rating.BAD,  # hypothetical?
    Rating.GOOD         : Rating.BAD,
    Rating.VERY_GOOD    : Rating.SOMEWHAT_BAD,
}


def negated_rating(rating: Rating) -> Rating:
    assert rating is not None
    return RATING_TO_NEGATED_RATING_MAP[rating]


def ranged_rating(rating_value: int) -> Rating:
    return Rating(min(_MAX_RATING_VALUE, max(_MIN_RATING_VALUE, rating_value)))
