"""
Tests for :py:mod:`shapiro.language`.
"""
from shapiro.language import (EnglishSentiment, GermanSentiment,
                              LanguageSentiment, language_sentiment_for)
from spacy.language import Language
from spacy.tokens import Token


def _token_for(nlp: Language, word: str) -> Token:
    return next(nlp(word).sents)[0]


def test_can_find_english_sentiments(nlp_en: Language):
    en = EnglishSentiment()
    assert en.is_diminisher(_token_for(nlp_en, 'slightly'))
    assert en.is_intensifier(_token_for(nlp_en, 'very'))
    assert en.is_negation(_token_for(nlp_en, 'not'))


def test_can_find_german_sentiments(nlp_de: Language):
    de = GermanSentiment()
    assert de.is_diminisher(_token_for(nlp_de, 'eher'))
    assert de.is_intensifier(_token_for(nlp_de, 'sehr'))
    assert de.is_negation(_token_for(nlp_de, 'nicht'))


def test_can_find_language_sentiment_for_code():
    assert type(language_sentiment_for('en')) == EnglishSentiment
    assert type(language_sentiment_for('en_US')) == EnglishSentiment
    assert type(language_sentiment_for('de')) == GermanSentiment
    assert type(language_sentiment_for('xx')) == LanguageSentiment
