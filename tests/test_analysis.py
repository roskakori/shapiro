"""
Tests for :py:mod:`shapiro.analysis`.
"""
from enum import Enum

import pytest
from shapiro import analysis, tools
from shapiro.analysis import Lexicon
from shapiro.common import Rating, RestaurantTopic
from shapiro.language import EnglishSentiment
from spacy.language import Language
from spacy.tokens import Token

_CHICKEN = 'chicken'


def _token_for(nlp: Language, word: str) -> Token:
    """
    Create a token for ``word``.
    """
    # TODO: Check if there is a more efficient way to do this.
    return next(nlp(word).sents)[0]


def test_can_match_exact_lexicon_entry(nlp_en: Language):
    chicken_token = _token_for(nlp_en, _CHICKEN)
    chicken_entry = analysis.LexiconEntry(_CHICKEN, RestaurantTopic.FOOD)
    assert tools.is_close(chicken_entry.matching(chicken_token), 1.0)


def test_can_match_regex_lexicon_entry(nlp_en: Language):
    chicken_token = _token_for(nlp_en, _CHICKEN)
    chicken_entry = analysis.LexiconEntry(f'.*{_CHICKEN.lower()}', RestaurantTopic.FOOD)
    assert chicken_entry.matching(chicken_token) >= 0.5


def test_can_read_lexicon_csv(nlp_en: Language, en_restauranteering_csv_path: str):
    lexicon = analysis.Lexicon(RestaurantTopic, Rating)
    lexicon.read_from_csv(en_restauranteering_csv_path)
    assert len(lexicon.entries) >= 1

    clean_token = _token_for(nlp_en, 'clean')
    clean_entry = lexicon.lexicon_entry_for(clean_token)
    assert clean_entry is not None


def test_fails_on_adding_lexicon_entry_with_unknown_topic():
    lexicon = analysis.Lexicon(RestaurantTopic, Rating)
    with pytest.raises(ValueError) as error:
        lexicon._append_lexicon_entry_from_row(['x', '', 'unknown'])
    assert error.match(r"^name 'unknown' for enum RestaurantTopic must be one of: .+$")


def test_fails_on_adding_lexicon_entry_with_unknown_rating():
    lexicon = analysis.Lexicon(RestaurantTopic, Rating)
    with pytest.raises(ValueError) as error:
        lexicon._append_lexicon_entry_from_row(['x', '', '', 'unknown'])
    assert error.match(r"^name 'unknown' for enum Rating must be one of: .+$")


def test_fails_on_duplicate_topic():
    class _BrokenTopic(Enum):
        some, SOME = range(2)

    with pytest.raises(ValueError) as error:
        analysis.Lexicon(_BrokenTopic, Rating)
    assert error.match(r"^case insensitive name 'SOME' for enum _BrokenTopic must be unique but clashes with 'some'$")


def test_can_convert_lexicon_entry_to_repr():
    lexicon_entry = analysis.LexiconEntry('tasty', RestaurantTopic.FOOD, analysis.Rating.GOOD)
    assert 'LexiconEntry(tasty, topic=FOOD, rating=GOOD)' == repr(lexicon_entry)


def test_can_count_lemmas_with_pos(nlp_en):
    counter = analysis.LemmaCounter(nlp_en, use_pos=True)
    counter.count('hello! hello 1! hello world!')
    assert counter.lemma_pos_to_count_map == {
        ('hello', 'INTJ'): 3,
        ('world', 'NOUN'): 1
    }


def test_can_count_lemmas_without_pos(nlp_en):
    counter = analysis.LemmaCounter(nlp_en, use_pos=False)
    counter.count('hello! hello 1! hello world!')
    assert counter.lemma_pos_to_count_map == {
        ('hello', None): 3,
        ('world', None): 1
    }


def test_can_ignore_stopwords(nlp_en):
    counter = analysis.LemmaCounter(nlp_en, count_stopwords=False, use_pos=False)
    counter.count('This is the best soap.')
    assert counter.lemma_pos_to_count_map == {
        ('good', None): 1,
        ('soap', None): 1,
    }


def test_can_count_stopwords(nlp_en):
    counter = analysis.LemmaCounter(nlp_en, count_stopwords=True, use_pos=False)
    counter.count('This is the best soap.')
    assert counter.lemma_pos_to_count_map == {
        ('this', None): 1,
        ('be', None): 1,
        ('the', None): 1,
        ('good', None): 1,
        ('soap', None): 1,
    }


def test_can_find_opinions(nlp_en: Language, lexicon_restauranteering: Lexicon, english_sentiment: EnglishSentiment):
    feedback_text = """The schnitzel was not very tasty.
        The waiter was polite.
        The football game ended 2:1."""
    opinion_miner = analysis.OpinionMiner(nlp_en, lexicon_restauranteering, english_sentiment, RestaurantTopic)
    opinions = opinion_miner.opinions(feedback_text)
    opinions_with_text = [
        (topic, rating, str(sent).strip())
        for topic, rating, sent in opinions
    ]
    assert opinions_with_text == [
        (RestaurantTopic.FOOD, Rating.SOMEWHAT_BAD, 'The schnitzel was not very tasty.'),
        (RestaurantTopic.SERVICE, Rating.GOOD, 'The waiter was polite.'),
        (None, None, 'The football game ended 2:1.')
    ]


def test_can_find_opinions_with_idioms(
        nlp_en: Language, lexicon_restauranteering: Lexicon, english_sentiment: EnglishSentiment):
    feedback_text = 'The schnitzel was not up to par with other restaurants.'
    opinion_miner = analysis.OpinionMiner(nlp_en, lexicon_restauranteering, english_sentiment, RestaurantTopic)
    opinions = opinion_miner.opinions(feedback_text)
    opinions_with_text = [
        (topic, rating, str(sent).strip())
        for topic, rating, sent in opinions
    ]
    assert opinions_with_text == [
        (RestaurantTopic.FOOD, Rating.BAD, 'The schnitzel was not good with other restaurants.'),
    ]


def test_can_use_previous_topic_for_opinion(
        nlp_en: Language, lexicon_restauranteering: Lexicon, english_sentiment: EnglishSentiment):
    feedback_text = 'The waiter was very polite. He was not quick though.'
    opinion_miner = analysis.OpinionMiner(nlp_en, lexicon_restauranteering, english_sentiment, RestaurantTopic)
    opinions = opinion_miner.opinions(feedback_text)
    opinions_with_text = [
        (topic, rating, str(sent).strip())
        for topic, rating, sent in opinions
    ]
    assert opinions_with_text == [
        (RestaurantTopic.SERVICE, Rating.VERY_GOOD, 'The waiter was very polite.'),
        (RestaurantTopic.SERVICE, Rating.BAD, 'He was not quick though.'),
    ]


def test_can_use_expected_topic_for_opinion(
        nlp_en: Language, lexicon_restauranteering: Lexicon, english_sentiment: EnglishSentiment):
    feedback_text = 'They were very polite.'
    opinion_miner = analysis.OpinionMiner(nlp_en, lexicon_restauranteering, english_sentiment, RestaurantTopic)
    opinions = opinion_miner.opinions(feedback_text, RestaurantTopic.FOOD)
    opinions_with_text = [
        (topic, rating, str(sent).strip())
        for topic, rating, sent in opinions
    ]
    assert opinions_with_text == [
        (RestaurantTopic.SERVICE, Rating.VERY_GOOD, 'They were very polite.'),
    ]
