"""
Functions to preprocess sentences for sentiment analysis.
"""
import logging
import re
from typing import Dict, Pattern, Tuple

from shapiro import common, tools

#: Prefix used to mark unified emojis.
EMOJI_PREFIX = 'emoji__'

_log = tools.log


_DEFAULT_EMOTICONS_CSV_PATH = common.lexicon_path('emoticons_lexicon.csv')


def create_emoticon_to_name_and_rating_map(emoticons_csv_path: str=None) -> Dict[str, Tuple[str, common.Rating]]:
    """
    Mapping read from CSV file ``emoticons_csv_path`` for emoticon to a tuple
    with the name and the :py:class:`shapiro.common.Rating` assigned to it.

    If no ``emoticons_csv_path`` is specified, internal defaults are used.
    """
    result = {}
    actual_emoticons_csv_path = emoticons_csv_path if emoticons_csv_path is not None else _DEFAULT_EMOTICONS_CSV_PATH
    emoticon_to_row_index_map = {}
    _log.info('reading emoticons from "%s"', actual_emoticons_csv_path)
    for row_index, row in enumerate(common.csv_rows(actual_emoticons_csv_path)):
        emoticon, name, rating = _emoticon_name_and_rating_from_emtiocon_csv_row(
            actual_emoticons_csv_path, emoticon_to_row_index_map, row, row_index)
        result[emoticon] = (name, rating)
    return result


def _emoticon_name_and_rating_from_emtiocon_csv_row(
        emoticons_csv_path, emoticon_to_row_index_map, row, row_index):
    if len(row) < 3:
        raise common.OpinionCsvError(
            f'row must have at least 3 items: {row}', emoticons_csv_path, row_index)
    row = [item.strip() for item in row[:3]]
    for cell_index, cell in enumerate(row):
        if cell == '':
            raise common.OpinionCsvError(
                'cell must contain text', emoticons_csv_path, row_index, cell_index)
    emoticon, name, rating_name = row[:3]
    clashing_emoticon_row = emoticon_to_row_index_map.get(emoticon)
    if clashing_emoticon_row is not None:
        raise common.OpinionCsvError(
            f'emoticon "{emoticon}" must be unique but has already been defined in R{clashing_emoticon_row + 1}',
            row_index, 0)
    mappable_rating_name = rating_name.replace(' ', '_').upper()
    try:
        rating = common.Rating[mappable_rating_name]
    except KeyError:
        raise common.OpinionCsvError(
            f'rating "{mappable_rating_name}" (transformed from "{rating_name}") '
            f'must be one of {common.VALID_RATING_NAMES}',
            emoticons_csv_path, row_index, 2)
    name = name.replace(' ', '_')
    return emoticon, name, rating


def compiled_synonym_source_to_target_map(synonym_source_to_target_map: Dict[str, str]) -> Dict[Pattern, str]:
    assert synonym_source_to_target_map is not None

    return _compiled_source_pattern_to_target_word_map('synonym', synonym_source_to_target_map, r'\b')


def _compiled_source_pattern_to_target_word_map(
        name: str, synonym_source_to_target_map: Dict[str, str], regex_at_end: str) -> Dict[Pattern, str]:
    assert name is not None
    assert regex_at_end is not None

    result = {}
    if synonym_source_to_target_map is not None:
        for source_text, target_text in synonym_source_to_target_map.items():
            try:
                source_regex = re.compile(r'\b' + re.escape(source_text) + regex_at_end, re.IGNORECASE)
            except re.error as error:
                raise ValueError('cannot convert %s %r to regular expression: %s' % (name, source_text, error))
            result[source_regex] = target_text
    return result


def replaced_synonyms(sentence: str, synonym_source_pattern_to_target_word_map: Dict[Pattern, str]) -> str:
    assert sentence is not None
    assert synonym_source_pattern_to_target_word_map is not None

    return _replaced('synonym', sentence, synonym_source_pattern_to_target_word_map)


def _replaced(name: str, sentence: str, source_pattern_to_target_word_map: Dict[Pattern, str]) -> str:
    assert name is not None
    assert sentence is not None
    assert source_pattern_to_target_word_map is not None

    result = sentence
    is_debug = _log.isEnabledFor(logging.DEBUG)
    for source_word_pattern, target_word in source_pattern_to_target_word_map.items():
        possible_modified_sentence = source_word_pattern.sub(target_word, result)
        if possible_modified_sentence != result:
            if is_debug:
                _log.debug('  replaced %s %s by %r', name, source_word_pattern.pattern, target_word)
            result = possible_modified_sentence
    return result


def compiled_abbreviation_to_long_form_map(
        abbreviation_without_dot_to_long_form_map: Dict[str, str]
        ) -> Dict[Pattern, str]:
    assert abbreviation_without_dot_to_long_form_map is not None

    return _compiled_source_pattern_to_target_word_map('abbreviation', abbreviation_without_dot_to_long_form_map, r'\.')


def replaced_abbreviations(sentence: str,
                           abbreviation_pattern_to_full_text_map: Dict[str, str]) -> str:
    """
    Expand abbreviations terminated with a dot to its long form. Ideally spaCy
    already supports all the abbreviations you need, but in case some are
    missing, sentence borders might not be detected correctly anymore.

    This function provides a quick work around to deal with this situation.

    For a more permanent solution consider extending spaCy's exception lists,
    for example
    https://github.com/explosion/spaCy/blob/master/spacy/lang/de/tokenizer_exceptions.py.
    """
    assert sentence is not None
    assert abbreviation_pattern_to_full_text_map is not None

    return _replaced('abbreviation', sentence, abbreviation_pattern_to_full_text_map)


def unified_emoticons(text: str) -> str:
    assert text is not None

    result = text
    emoticon_to_name_map_and_rating = create_emoticon_to_name_and_rating_map()
    is_debug = _log.isEnabledFor(logging.DEBUG)
    for source_text, (target_text, _) in emoticon_to_name_map_and_rating.items():
        target_text = EMOJI_PREFIX + target_text + ' '
        old_result = result
        result = result.replace(source_text, target_text)
        if is_debug and (result != old_result):
            _log.debug(f'  unified emoticon {source_text} to {target_text}')
    return result
