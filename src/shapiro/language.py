"""
Language specific settings
"""
from typing import Dict, Set

from shapiro.common import Rating, ranged_rating
from shapiro.tools import log, signum
from spacy.tokens import Token

_log = log


class LanguageSentiment:
    def __init__(self, language_code: str):
        assert language_code is not None
        assert len(language_code) == 2, 'language code must have exactly 2 characters but is: %r' % language_code
        self.language_code = language_code
        self.diminishers: Set[str] = set()
        self.intensifiers: Set[str] = set()
        self.negatives: Dict[str, Rating] = {}
        self.positives: Dict[str, Rating] = {}
        self.idioms: Dict[str, Rating] = {}
        self.negations: Set[str] = set()
        self.rating_to_localized_text_map: Dict[Rating, str] = {}

    def diminished(self, rating: Rating) -> Rating:
        if abs(rating.value) > 1:
            return ranged_rating(rating.value - signum(rating.value))
        else:
            return rating

    def intensified(self, rating: Rating) -> Rating:
        if abs(rating.value) > 1:
            return ranged_rating(rating.value + signum(rating.value))
        else:
            return rating

    def is_intensifier(self, token: Token) -> bool:
        return token.lemma_.lower() in self.intensifiers

    def is_diminisher(self, token: Token) -> bool:
        return token.lemma_.lower() in self.diminishers

    def is_negation(self, token: Token) -> bool:
        return token.lemma_.lower() in self.negations


class EnglishSentiment(LanguageSentiment):
    def __init__(self):
        super().__init__('en')
        self.diminishers = {
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
        }
        self.intensifiers = {
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
        }
        self.negatives = {
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
        self.positives = {
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
        self.idioms = {
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
        self.negations = {
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
        }
        self.rating_to_localized_text_map = {
            rating: rating.name.lower().replace('_', ' ') for rating in Rating
        }


class GermanSentiment(LanguageSentiment):
    def __init__(self):
        super().__init__('de')
        self.diminishers = {
            'eher',
            'bisschen',
            'ein wenig',
            'einigermaßen',
            'etwas',
        }
        self.intensifiers = {
            'absolut',
            'besonders',
            'extrem',
            'sehr',
            'total',
            'voll',
            'vollkommen',
            'wirklich',
            'ziemlich',
            'zu',
        }
        self.negatives = {
            'ausbaufähig': Rating.BAD,
            'Bedenken': Rating.SOMEWHAT_BAD,
            'beschissen': Rating.VERY_BAD,
            'durchschnittlich': Rating.SOMEWHAT_BAD,
            'furchtbar': Rating.VERY_BAD,
            'ineffizient': Rating.BAD,
            'mau': Rating.SOMEWHAT_BAD,
            'mühsam': Rating.SOMEWHAT_BAD,
            'obwohl': Rating.BAD,
            'schal': Rating.BAD,
            'schlecht': Rating.BAD,
            'uncharmant': Rating.BAD,
            'uneffektiv': Rating.BAD,
            'ungut': Rating.BAD,
            'unschön': Rating.SOMEWHAT_BAD,
            'übel': Rating.BAD,
            'unterdurchschnittlich': Rating.BAD,
            'verbesserungsfähig': Rating.BAD,
            'verbesserungswürdig': Rating.BAD,
            'wünschenswert': Rating.BAD,

            # TODO: Add special logic for modals.
            'können': Rating.SOMEWHAT_BAD,
            'müssen': Rating.SOMEWHAT_BAD,
            'sollen': Rating.SOMEWHAT_BAD,
            'wär': Rating.SOMEWHAT_BAD,
            'wäre': Rating.SOMEWHAT_BAD,
            'wären': Rating.SOMEWHAT_BAD,
            'wärn': Rating.SOMEWHAT_BAD,
        }
        self.positives = {
            'ausgezeichnet': Rating.VERY_GOOD,
            'bestens': Rating.VERY_GOOD,
            'Charme': Rating.GOOD,
            'charmant': Rating.GOOD,
            'cool': Rating.GOOD,
            'entzückend': Rating.VERY_GOOD,
            'effektiv': Rating.GOOD,
            'effizient': Rating.GOOD,
            'exzellent': Rating.VERY_GOOD,
            'fantastisch': Rating.VERY_GOOD,
            'geil': Rating.GOOD,
            'gern': Rating.GOOD,
            'gut': Rating.GOOD,
            'kompetent': Rating.GOOD,
            'lässig': Rating.GOOD,
            'leiwand': Rating.GOOD,
            'nett': Rating.GOOD,
            'ok': Rating.SOMEWHAT_GOOD,
            'okay': Rating.SOMEWHAT_GOOD,
            'passen': Rating.GOOD,
            'perfekt': Rating.VERY_GOOD,
            'prima': Rating.VERY_GOOD,
            'reichhaltig': Rating.GOOD,
            'reizend': Rating.GOOD,
            'super': Rating.VERY_GOOD,
            'toll': Rating.VERY_GOOD,
            'top': Rating.VERY_GOOD,
            'überdurchschnittlich': Rating.SOMEWHAT_GOOD,
            'überzeugend': Rating.SOMEWHAT_GOOD,
            'vorzüglich': Rating.VERY_GOOD,
            'weiterempfehlen': Rating.VERY_GOOD,
            'wunderbar': Rating.VERY_GOOD,
            'zufrieden': Rating.SOMEWHAT_GOOD
        }
        self.idioms = {
            'gerne wieder': Rating.GOOD,
            'Gold wert': Rating.VERY_GOOD,
            'ist spitze': Rating.VERY_GOOD,
            'könnte etwas Liebe vertragen': Rating.SOMEWHAT_BAD,
            'luft nach oben': Rating.SOMEWHAT_GOOD,
            'vom Hocker gerissen': Rating.VERY_GOOD,
            'weiter so!': Rating.GOOD,
            'wenig berauschend': Rating.SOMEWHAT_BAD,
            'würde wieder': Rating.GOOD,
        }
        self.negations = {
            'kein',
            'keine',
            'keiner',
            'keines',
            'nicht',
        }
        self.rating_to_localized_text_map = {
            Rating.VERY_GOOD: 'sehr gut',
            Rating.GOOD: 'gut',
            Rating.SOMEWHAT_GOOD: 'eher gut',
            Rating.SOMEWHAT_BAD: 'eher schlecht',
            Rating.BAD: 'schlecht',
            Rating.VERY_BAD: 'sehr schlecht',
        }


def language_sentiment_for(language_code: str) -> LanguageSentiment:
    base_code = language_code.split('_')[0]
    if len(base_code) != 2:
        raise ValueError(
            'language base code must be exactly 2 letters but is: %r (derived from %r)'
            % (base_code, language_code))
    if base_code == 'en':
        result = EnglishSentiment()
    elif base_code == 'de':
        result = GermanSentiment()
    else:
        _log.warning('cannot find language sentiment for %r, using empty default sentiment')
        result = LanguageSentiment(base_code)
    return result
