"""
Language specific settings
"""
from shapiro.common import Rating


class LanguageSentiment:
    diminishers = []
    intensifiers = []
    negatives = []
    positives = []
    turners = []


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
