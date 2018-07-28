"""
Functions to preprocess sentences for sentiment analysis.
"""
import csv
import logging
import re
from enum import Enum
from typing import Any, Dict, List, Pattern, Union

import spacy
from spacy.language import Language
from spacy.tokens import Token

from shapiro import tools

#: Prefix used to mark unified emojis.
EMOJI_PREFIX = 'emoji__'

_log = tools.log


_WESTERN_SMILEY_TO_EMOJI_NAME_MAP = {
    ':)': 'slight_smile',
    ':-)': 'slight_smile',
    '=)': 'slight_smile',
    ':(': 'slight_frown',
    ':-(': 'slight_frown',
    ':D': 'smile',
    ':-D': 'smile',
    ':P': 'stuck_out_tongue',
    ':-P': 'stuck_out_tongue',
    ';)': 'wink',
    ';-)': 'wink',
}

_EASTERN_SMILEY_TO_EMOJI_NAME_MAP = {
    '^^': 'slight_smile',
    '^_^': 'slight_smile',
}
#: Unicode emojis, see also: http://www.unicode.org/emoji/charts/full-emoji-list.html
_EMOJI_TO_NAME_MAP = {
    '\U0001F642': 'slight_smile',  # ☺
}


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


def compiled_abbreviation_to_long_form_map(abbreviation_without_dot_to_long_form_map: Dict[str, str]) -> Dict[Pattern, str]:
    assert abbreviation_without_dot_to_long_form_map is not None

    return _compiled_source_pattern_to_target_word_map('abbreviation', abbreviation_without_dot_to_long_form_map, r'\.')


def replaced_abbreviations(sentence: str, abbreviation_pattern_to_full_text_map: Dict[str, str]) -> str:
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


def unified_emojis(text: str, unify_western_smileys=True, unify_eastern_smileys=True) -> str:
    assert text is not None

    emoji_to_name_map = dict(_EMOJI_TO_NAME_MAP)
    if unify_eastern_smileys:
        emoji_to_name_map.update(_EASTERN_SMILEY_TO_EMOJI_NAME_MAP)
    if unify_western_smileys:
        emoji_to_name_map.update(_WESTERN_SMILEY_TO_EMOJI_NAME_MAP)
    result = text

    is_debug = _log.isEnabledFor(logging.DEBUG)
    for source_text, target_text in emoji_to_name_map.items():
        target_text = EMOJI_PREFIX + target_text + ' '
        old_result = result
        result = result.replace(source_text, target_text)
        if is_debug and (result != old_result):
            _log.debug('unified emoji %r to %s', source_text, target_text)
    return result

