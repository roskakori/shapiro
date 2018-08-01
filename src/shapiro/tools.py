"""
Various tools to make life easier.
"""
import argparse
import logging

#: The general logger used by all modules.
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


def add_language_argument(parser: argparse.ArgumentParser):
    """
    Add ``--language`` to an :class:`argparse.ArgumentParser` that refers to a
    2 letter `ISO-639-1 language code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_
    for witch spacy must provide a matching :class:`spacy.language.Language`.
    """
    parser.add_argument('--language', '-l', default='en',
                        help='two letter ISO-639-1 language code for spaCy; default: %(default)s')
