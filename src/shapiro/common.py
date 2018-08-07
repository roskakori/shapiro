"""
Common structures and function used by multiple modules.
"""
import csv
import os
from enum import Enum
from typing import Generator, List, Sequence

from spacy.tokens import Token


class OpinionError(Exception):
    """
    Error when processing opinion related data or resources.
    """
    pass


class OpinionCsvError(OpinionError):
    """
    Error when reading or writing opinion related data from / to CSV files.
    """
    def __init__(self, message, csv_path, row_index: int=None, cell_index: int=None):
        if row_index is None:
            assert cell_index is None
        assert row_index is None or row_index >= 0
        assert cell_index is None or cell_index >= 0

        full_message = csv_path
        if row_index is not None:
            full_message += f' (R{row_index + 1}'
            if cell_index is not None:
                full_message += f'C{cell_index + 1}'
            full_message += ')'
        full_message += f': {message}'
        super().__init__(full_message)


class Rating(Enum):
    VERY_BAD = -3
    BAD = -2
    SOMEWHAT_BAD = -1
    SOMEWHAT_GOOD = 1
    GOOD = 2
    VERY_GOOD = 3


#: Names of valid ratings (to be used for error messages).
VALID_RATING_NAMES = ', '.join(sorted([rating.name for rating in Rating]))


# FIXME: Remove this and make all functions using it able to work with a dynamic topic system.
class RestaurantTopic(Enum):
    AMBIENCE, FOOD, GENERAL, HYGIENE, SERVICE, VALUE = range(1, 7)


_MIN_RATING_VALUE = Rating.VERY_BAD.value
_MAX_RATING_VALUE = Rating.VERY_GOOD.value

#: Folder where standard lexicons are stored.
LEXICONS_FOLDER = os.path.join(os.path.dirname(__file__), 'lexicons')

#: Encoding for CSV files.
CSV_ENCODING = 'utf-8'

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


def lexicon_path(name: str) -> str:
    return os.path.join(LEXICONS_FOLDER, name)


def csv_rows(source_csv_path: str) -> Generator[List[str], None, None]:
    """
    Rows stored in a CSV file.
    """
    with open(source_csv_path, encoding=CSV_ENCODING, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            row = [cell.strip() for cell in row]
            is_empty_row = ''.join(row) == ''
            if not is_empty_row:
                is_comment = row[0].lstrip().startswith('#')
                if not is_comment:
                    yield row


def csv_writer(target_csv_file):
    return csv.writer(target_csv_file, delimiter=',', quotechar='"')


def write_csv_rows(target_csv_path: str, rows: Sequence[List[str]]):
    with open(target_csv_path, 'w', encoding=CSV_ENCODING, newline='') as target_csv_file:
        target_csv_writer = csv_writer(target_csv_file)
        for row in rows:
            target_csv_writer.writerow(row)
