"""
Common structures and function used by multiple modules.
"""
from enum import Enum

from spacy.tokens import Token


class Rating(Enum):
    VERY_BAD = -3
    BAD = -2
    SOMEWHAT_BAD = -1
    SOMEWHAT_GOOD = 1
    GOOD = 2
    VERY_GOOD = 3


# FIXME: Remove this and make all functions using it able to work with a dynamic topic system.
class RestaurantTopic(Enum):
    AMBIANCE, FOOD, GENERAL, HYGIENE, SERVICE, VALUE = range(6)


_MIN_RATING_VALUE = Rating.VERY_BAD.value
_MAX_RATING_VALUE = Rating.VERY_GOOD.value

RATING_TO_NEGATED_RATING_MAP = {
    Rating.VERY_BAD: Rating.SOMEWHAT_GOOD,
    Rating.BAD: Rating.GOOD,
    Rating.SOMEWHAT_BAD: Rating.GOOD,  # hypothetical?
    Rating.SOMEWHAT_GOOD: Rating.BAD,  # hypothetical?
    Rating.GOOD: Rating.BAD,
    Rating.VERY_GOOD: Rating.SOMEWHAT_BAD,
}


def negated_rating(rating: Rating) -> Rating:
    """
    Derived :py:class:`Rating` after a negation is applied.
    """
    assert rating is not None
    return RATING_TO_NEGATED_RATING_MAP[rating]


def ranged_rating(rating_value: int) -> Rating:
    """
    A :py:class:`Rating` based on matching ``int`` enum code of
    ``rating_value``. If ``rating_value`` is outside of the valid enum range
    it is automatically changed to an appropriate ``VERY_xxx``.
    """
    assert rating_value, 'rating_value=%r' % rating_value
    return Rating(min(_MAX_RATING_VALUE, max(_MIN_RATING_VALUE, rating_value)))


def debugged_token(token: Token) -> str:
    """
    Human readable string representation of ``token`` including shapiro
    specific extension attributes.
    """
    result = 'Token(%s, lemma=%s, pos=%s' % (token.text, token.lemma_, token.pos_)
    if token._.topic is not None:
        result += ', topic=' + token._.topic.name
    if token._.rating is not None:
        result += ', rating=' + token._.rating.name
    if token._.is_diminisher:
        result += ', diminisher'
    if token._.is_intensifier:
        result += ', intensifier'
    if token._.is_negation:
        result += ', negation'
    result += ')'
    return result
