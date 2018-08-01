"""
Language specific settings
"""
from shapiro.common import Rating, ranged_rating
from shapiro.tools import signum
from spacy.tokens import Token


class LanguageSentiment:
    diminishers = []
    intensifiers = []
    negatives = {}
    positives = {}
    idioms = {}
    negators = []

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
        'a little bit',
        'a little',
        'almost',
        'barely',
        'fairly',
        'hardly',
        'just enough',
        'kind of',
        'kind-of',
        'kinda',
        'kindof',
        'less',
        'marginally',
        'minimally',
        'mostly',
        'occasionally',
        'partly',
        'pretty',
        'scarcely',
        'slightly',
        'somewhat',
        'sort of',
        'sort-of',
        'sorta',
        'sortof',
    ]
    intensifiers = [
        'absolutely',
        'amazingly',
        'awfully',
        'completely',
        'considerably',
        'decidedly',
        'deeply',
        'dreadfully',
        'effing',
        'enormously',
        'entirely',
        'especially',
        'exceptionally',
        'extremely',
        'fabulously',
        'flippin',
        'flipping',
        'frickin',
        'fricking',
        'friggin',
        'frigging',
        'fucking',
        'fully',
        'greatly',
        'hella',
        'highly',
        'hugely',
        'incredibly',
        'intensely',
        'majorly',
        'more',
        'most',
        'particularly',
        'purely',
        'quite',
        'really',
        'remarkably',
        'so',
        'substantially',
        'terribly',
        'thoroughly',
        'totally',
        'tremendously',
        'uber',
        'unbelievably',
        'unusually',
        'utterly',
        'very',
    ]
    negatives = {
        'appalling': Rating.VERY_BAD,
        'awful': Rating.VERY_BAD,
        'bad': Rating.BAD,
        'disgusting': Rating.VERY_BAD,
        'dreadful': Rating.VERY_BAD,
        'foul': Rating.VERY_BAD,
        'poor': Rating.BAD,
        'subpar': Rating.BAD,
        'terrible': Rating.VERY_BAD,
        'unusual': Rating.BAD,
    }
    positives = {
        'amazing': Rating.VERY_GOOD,
        'awesome': Rating.VERY_GOOD,
        'excellent': Rating.VERY_GOOD,
        'exceptional': Rating.VERY_GOOD,
        'fabulous': Rating.VERY_GOOD,
        'good': Rating.GOOD,
        'great': Rating.VERY_GOOD,
        'incredible': Rating.VERY_GOOD,
        'nice': Rating.GOOD,
        'remarkable': Rating.VERY_GOOD,
        'special': Rating.GOOD,
        'thorough': Rating.VERY_GOOD,
        'tremendous': Rating.VERY_GOOD,
        'wonderful': Rating.VERY_GOOD,
    }
    idioms = {
        "don't give up your day job": Rating.VERY_BAD,
        'add insult to injury': Rating.VERY_BAD,
        'back handed': Rating.VERY_BAD,
        'back to the drawing board': Rating.VERY_BAD,
        'barking up the wrong tree': Rating.BAD,
        'benefit of the doubt': Rating.BAD,
        'better late than never': Rating.BAD,
        'bite the bullet': Rating.BAD,
        'blessing in disguise': Rating.GOOD,
        'cooking with gas': Rating.VERY_GOOD,
        'cost an arm and a leg': Rating.VERY_BAD,
        'cut corners': Rating.VERY_BAD,
        'cut the mustard': Rating.GOOD,
        'cutting corners': Rating.VERY_BAD,
        'elephant in the room': Rating.BAD,
        'far cry from': Rating.VERY_BAD,
        'get your act together': Rating.VERY_BAD,
        'hit the nail on the head': Rating.VERY_GOOD,
        'kiss of death': Rating.VERY_BAD,
        'last straw': Rating.VERY_BAD,
        'missed the boat': Rating.VERY_BAD,
        'not rocket science': Rating.BAD,
        'nothing better than': Rating.VERY_GOOD,
        'old fashioned': Rating.BAD,
        'on the ball': Rating.VERY_GOOD,
        'out of hand': Rating.VERY_BAD,
        'pull your socks up': Rating.VERY_BAD,
        'the bomb': Rating.VERY_GOOD,
        'the cold shoulder': Rating.VERY_BAD,
        'under the weather': Rating.BAD,
        'up to par': Rating.GOOD,
        'wild goose chase': Rating.BAD,
        'yeah right': Rating.BAD,
    }
    negators = [
        'ain\'t',
        'aint',
        'aren\'t',
        'arent',
        'can\'t',
        'cannot',
        'cant',
        'couldn\'t',
        'couldnt',
        'daren\'t',
        'darent',
        'despite',
        'didn\'t',
        'didnt',
        'doesn\'t',
        'doesnt',
        'don\'t',
        'dont',
        'hadn\'t',
        'hadnt',
        'hasn\'t',
        'hasnt',
        'haven\'t',
        'havent',
        'isn\'t',
        'isnt',
        'mightn\'t',
        'mightnt',
        'mustn\'t',
        'mustnt',
        'needn\'t',
        'neednt',
        'neither',
        'never',
        'no',
        'none',
        'nope',
        'nor',
        'not',
        'not',
        'nothing',
        'nowhere',
        'oughtn\'t',
        'oughtnt',
        'rarely',
        'seldom',
        'shan\'t',
        'shant',
        'shouldn\'t',
        'shouldnt',
        'uh-uh',
        'wasn\'t',
        'wasnt',
        'weren\'t',
        'werent',
        'without',
        'won\'t',
        'wont',
        'wouldn\'t',
        'wouldnt',
    ]

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
    idioms = {}
    negators = [
        'kein',
        'keine',
        'keiner',
        'keines',
        'nicht',
    ]
