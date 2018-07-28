"""
Language specific settings
"""
from spacy.token import Token
from shapiro.common import Rating, ranged_rating
from shapiro.tools import signum


class LanguageSentiment:
    diminishers = []
    intensifiers = []
    negatives = []
    positives = []
    turners = []

    @staticmethod
    def diminished(rating: Rating) -> Rating:
        if abs(rating.value) > 1:
            return ranged_rating(rating.value - signum(rating.value))
        else:
            return rating

    @staticmethod
    def intensified(rating: Rating) -> Rating:
        if abs(rating.value) > 1:
            return ranged_rating(rating.value + signum(rating.value))
        else:
            return rating


class EnglishSentiment(LanguageSentiment):
    diminishers = [
        # TODO #2: 'a little',
        # TODO #2: 'a little bit',
        'barely',
        'pretty',  # TODO #3
        'slightly',
        'somewhat',
    ]
    intensifiers = [
        'awfully',
        'dreadfully',
        'extremely',
        'really',
        'so',  # TODO #3
        'terribly',
        'very',
    ]
    negatives = {
        'bad': Rating.BAD,
        'poor': Rating.BAD,
        'terrible': Rating.VERY_BAD,
    }
    positives = {
        'amazing': Rating.VERY_GOOD,
        'excellent': Rating.VERY_GOOD,
        'good': Rating.GOOD,
        'nice': Rating.GOOD,
        'wonderful': Rating.VERY_GOOD,
    }
    turners = [
        'no',
        'not',
    ]
    negators = {
        'no',
        'not',
        'none',
    }

    @staticmethod
    def is_intensifier(token: Token) -> bool:
        return token.lemma_.lower() in EnglishSentiment.intensifiers

    @staticmethod
    def is_diminisher(token: Token) -> bool:
        return token.lemma_.lower() in EnglishSentiment.diminishers

    @staticmethod
    def is_negation(token: Token) -> bool:
        return token.lemma_.lower() in EnglishSentiment.negators


class GermanSentiment(LanguageSentiment):
    diminishers = [
        'eher',  # TODO #3
        'ein wenig',   # TODO: support multiple words
        'ein kleines bißchen',    # TODO: support multiple words
        'einigermaßen',  # TODO #3
        'etwas',  # TODO #3
    ]
    intensifiers = [
        'extrem',
        'wirklich',
        'sehr',
        'zu',  # TODO #3
    ]
    negatives = {
        'furchtbar': Rating.VERY_BAD,
        'beschissen': Rating.VERY_BAD,
        'schlecht': Rating.BAD,
    }
    positives = {
        'exzellent': Rating.VERY_GOOD,
        'gut': Rating.GOOD,
        'wunderbar': Rating.VERY_GOOD,
    }
    turners = [
        'kein',
        'keine',
        'keiner',
        'keines',
        'nicht',
    ]
