"""
Tests for :py:mod:`shapiro.preprocess`.
"""
from shapiro import common, preprocess


def test_can_replace_synonyms():
    synonyms = {
        'laptop': 'notebook',
        'junk': 'crap',
    }
    compiled_synonyms = preprocess.compiled_synonym_source_to_target_map(synonyms)
    assert 'this notebook rocks' == preprocess.replaced_synonyms('this laptop rocks', compiled_synonyms)
    assert 'nothing to see here' == preprocess.replaced_synonyms('nothing to see here', compiled_synonyms)


def test_can_unify_emoticons():
    expected_text = 'smile: emoji__happy_face , ' \
                    'smile more: emoji__slightly_smiling_face , ' \
                    'smile again: emoji__slightly_smiling_face '
    assert expected_text == preprocess.unified_emoticons('smile: :-), smile more: ^^, smile again: \U0001F642')


def test_can_replace_abbreviations():
    # NOTE: By now this are fictional examples because as of version 2.0.11 spaCy supports them out of the box.
    abbreviation_to_long_form_map = {
        'ca': 'circa',  # German/Latin for "approximately"
        'ev': 'eventuell',  # German for "possibly"
        'z.B': 'zum Beispiel',  # German for "zum Beispiel"
    }
    abbreviation_pattern_to_long_form_map = \
        preprocess.compiled_abbreviation_to_long_form_map(abbreviation_to_long_form_map)
    assert len(abbreviation_to_long_form_map) == len(abbreviation_pattern_to_long_form_map)

    assert 'Das wäre eventuell angenehm' \
        == preprocess.replaced_abbreviations('Das wäre ev. angenehm', abbreviation_pattern_to_long_form_map)
    assert 'sehr freundlich, zum Beispiel Josef' \
        == preprocess.replaced_abbreviations('sehr freundlich, z.B. Josef', abbreviation_pattern_to_long_form_map)


def test_can_create_default_emoticon_to_name_and_rating_map():
    emoticon_to_name_and_rating_map = preprocess.create_emoticon_to_name_and_rating_map()
    assert len(emoticon_to_name_and_rating_map) != 0
    assert '🙂' in emoticon_to_name_and_rating_map
    assert emoticon_to_name_and_rating_map['🙂'] == ('slightly_smiling_face', common.Rating.SOMEWHAT_GOOD)
