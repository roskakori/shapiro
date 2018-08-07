"""
Tests for :py:mod:`shapiro.common`.
"""
from shapiro.common import (OpinionCsvError, Rating, negated_rating,
                            ranged_rating)


def test_can_limit_rating_to_valid_range():
    assert ranged_rating(Rating.VERY_GOOD.value) == Rating.VERY_GOOD
    assert ranged_rating(Rating.VERY_GOOD.value + 1) == Rating.VERY_GOOD

    assert ranged_rating(Rating.VERY_BAD.value) == Rating.VERY_BAD
    assert ranged_rating(Rating.VERY_BAD.value - 1) == Rating.VERY_BAD

    assert ranged_rating(Rating.SOMEWHAT_GOOD.value) == Rating.SOMEWHAT_GOOD


def test_can_negate_rating():
    assert negated_rating(Rating.GOOD) == Rating.BAD
    assert negated_rating(Rating.VERY_BAD) == Rating.SOMEWHAT_GOOD


def test_can_render_opinion_csv_error():
    assert str(OpinionCsvError('x must be y', 'some.csv')) == 'some.csv: x must be y'
    assert str(OpinionCsvError('x must be y', 'some.csv', 3)) == 'some.csv (R4): x must be y'
    assert str(OpinionCsvError('x must be y', 'some.csv', 3, 5)) == 'some.csv (R4C6): x must be y'
