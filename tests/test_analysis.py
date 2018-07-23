"""
Tests for analysis module.
"""
from enum import Enum

import pytest
from spacy.language import Language
from spacy.tokens.token import Token

from shapiro import analysis
from shapiro import tools


_CHICKEN = 'chicken'


class _Topic(Enum):
    GENERAL, FOOD, HYGIENE, SERVICE = range(4)


class _Rating(Enum):
    VERY_BAD = -3
    BAD = -2
    SOMEWHAT_BAD = -1
    SOMEWHAT_GOOD = 1
    GOOD = 2
    VERY_GOOD = 3


def _token_for(nlp: Language, word: str) -> Token:
    # TODO: Check if there is a more efficient way to do this.
    return next(nlp(word).sents)[0]


def test_can_match_exact_lexicon_entry(nlp_en: Language):
    chicken_token = _token_for(nlp_en, _CHICKEN)
    chicken_entry = analysis.LexiconEntry(_CHICKEN, _Topic, None)
    assert tools.is_close(chicken_entry.matching(chicken_token), 1.0)


def test_can_read_lexicon_csv(nlp_en: Language, en_restauranteering_csv_path: str):
    lexicon = analysis.Lexicon(_Topic, _Rating)
    lexicon.read_from_csv(en_restauranteering_csv_path)
    assert len(lexicon.entries) >= 1

    clean_token = _token_for(nlp_en, 'clean')
    clean_entry = lexicon.lexicon_entry_for(clean_token)
    assert clean_entry is not None


def test_fails_on_adding_lexicon_entry_with_unknown_topic():
    lexicon = analysis.Lexicon(_Topic, _Rating)
    with pytest.raises(ValueError) as error:
        lexicon._append_lexicon_entry_from_row(['x', 'unknown'])
    assert error.match(r"^name 'unknown' for enum _Topic must be one of: .+$")


def test_fails_on_adding_lexicon_entry_with_unknown_rating():
    lexicon = analysis.Lexicon(_Topic, _Rating)
    with pytest.raises(ValueError) as error:
        lexicon._append_lexicon_entry_from_row(['x', '', 'unknown'])
    assert error.match(r"^name 'unknown' for enum _Rating must be one of: .+$")


def test_fails_on_duplicate_topic():
    class _BrokenTopic(Enum):
        some, SOME = range(2)

    with pytest.raises(ValueError) as error:
        analysis.Lexicon(_BrokenTopic, _Rating)
    assert error.match(r"^case insensitive name 'some' for enum _BrokenTopic must be unique$")


def test_can_replace_synonyms():
    synonyms = {
        'laptop': 'notebook',
        'junk': 'crap',
    }
    compiled_synonyms = analysis.compiled_synonym_source_to_target_map(synonyms)
    assert 'this notebook rocks' == analysis.replaced_synonyms('this laptop rocks', compiled_synonyms)
    assert 'nothing to see here' == analysis.replaced_synonyms('nothing to see here', compiled_synonyms)


def test_can_unify_emojis():
    assert 'smile: __emoji_slight_smile , smile more: __emoji_slight_smile , smile again: __emoji_slight_smile ' == \
        analysis.unified_emojis('smile: :-), smile more: ^^, smile again: \U0001F642')
