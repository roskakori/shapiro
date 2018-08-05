"""
Types and functions for sentiment analysis.
"""
import csv
import re
from enum import Enum
from typing import Dict, Generator, List, Pattern, Sequence, Tuple, Union

import spacy
from shapiro import tools
from shapiro.common import Rating, debugged_token, negated_rating
from shapiro.language import LanguageSentiment
from shapiro.preprocess import (compiled_idiom_to_localized_rating_text_map,
                                create_emoticon_to_name_and_rating_map,
                                replaced_idioms)
from spacy.language import Language
from spacy.tokens import Token

_log = tools.log


def most_common_lemmas(
        nlp: Language, text: Union[str, Sequence[str]],
        number: int=20, count_stopwords: bool=False, use_pos: bool=False) \
        -> Sequence[Tuple[int, Tuple[str, str]]]:
    counter = LemmaCounter(nlp, count_stopwords=count_stopwords, use_pos=use_pos)
    texts_to_count = [text] if type(text) == str else text
    for text_to_count in texts_to_count:
        counter.count(text_to_count)
    else:
        result = []
    result = sorted([
        (count, lemma, pos)
        for (lemma, pos), count in counter.lemma_pos_to_count_map.items()
    ], reverse=True)
    if number != 0:
        result = result[:number]
    return result


class LemmaCounter:
    """
    Counter for pairs of lemmas and part of speech tags in a text only
    considering tokens that start with a (Unicode) letter.
    """
    def __init__(self, nlp: Language, count_stopwords: bool=False, use_pos: bool=False):
        assert nlp is not None

        self.lemma_pos_to_count_map = {}
        self._nlp = nlp
        self._use_pos = use_pos
        self._count_stopwords = count_stopwords
        self._stopwords = nlp.Defaults.stop_words

    def count(self, text: str):
        document = self._nlp(text)
        for sent in document.sents:
            for token in sent:
                is_stop = token.is_stop or token.lemma_.lower() in self._nlp.Defaults.stop_words
                if self._count_stopwords or not is_stop:
                    lemma = token.lemma_
                    is_proper_word = (len(lemma) >= 1) and lemma[0].isalpha()
                    if is_proper_word:
                        pos = token.pos_ if self._use_pos else None
                        key = (lemma, pos)
                        if key in self.lemma_pos_to_count_map:
                            self.lemma_pos_to_count_map[key] += 1
                        else:
                            self.lemma_pos_to_count_map[key] = 1


class LexiconEntry:
    """
    Entry in a lexicon that can be compared with a token.
    """
    _IS_REGEX_REGEX = re.compile(r'.*[.+*\[$^\\]')

    def __init__(self, lemma: str, topic: Enum, rating: Rating):
        assert lemma is not None
        self.lemma = lemma
        self._lower_lemma = lemma.lower()
        self.topic = topic
        self.rating = rating
        self.is_regex = LexiconEntry._IS_REGEX_REGEX.match(self.lemma) is not None
        self._regex = re.compile(lemma) if self.is_regex else None

    def matching(self, token: Token) -> float:
        """
        A weight between 0.0 and 1.0 on how much ``token`` matches this entry.
        """
        assert token is not None
        result = 0.0
        if self.is_regex:
            if self._regex.match(token.text):
                result = 0.6
            elif self._regex.match(token.lemma_):
                result = 0.5
        else:
            if token.text == self.lemma:
                result = 1.0
            elif token.text.lower() == self.lemma:
                result = 0.9
            elif token.lemma_ == self.lemma:
                result = 0.8
            elif token.lemma_.lower() == self.lemma:
                result = 0.7
        return result

    def __str__(self) -> str:
        result = 'LexiconEntry(%s' % self.lemma
        if self.topic is not None:
            result += ', topic=%s' % self.topic.name
        if self.rating is not None:
            result += ', rating=%s' % self.rating.name
        if self.is_regex:
            result += ', is_regex=%s' % self.is_regex
        result += ')'
        return result

    def __repr__(self) -> str:
        return self.__str__()


class Lexicon:
    """
    Collection of :py:class:`LexiconEntry` that can be searched for a best match.
    """
    def __init__(self, topic_enum: Enum, rating_enum: Enum=Rating):
        assert topic_enum is not None
        assert rating_enum is not None

        def check_enum_names_are_case_insensitely_unique(enum_type: Enum):
            lower_name_to_name_map = {}
            for enum_entry in enum_type:
                lower_enum_entry_name = enum_entry.name.lower()
                clashing_name = lower_name_to_name_map.get(lower_enum_entry_name)
                if clashing_name is not None:
                    raise ValueError(
                        'case insensitive name %r for enum %s must be unique but clashes with %r'
                        % (enum_entry.name, enum_type.__name__, clashing_name)
                    )
                lower_name_to_name_map[lower_enum_entry_name] = enum_entry.name

        check_enum_names_are_case_insensitely_unique(topic_enum)
        check_enum_names_are_case_insensitely_unique(rating_enum)
        self.entries: List[LexiconEntry] = []
        self._topic_enum = topic_enum
        self._rating_enum = rating_enum

    def read_from_csv(self, lexicon_csv_path: str, encoding: str='utf-8', **csv_reader_keyword_arguments):
        """
        Append lexicon entries from CSV with columns for lemma, topic and
        rating. If the lemma is missing or starts with '#' the whole row is
        ignored. Leading and trailing white space is ignored. Upper and lower
        case on topics and ratings is ignored.

        :param lexicon_csv_path:
            path to the CSV file to read
        :param encoding:
            encoding of the CSV file
        :param csv_reader_keyword_arguments:
            additional options for the CSV reader, for example
            ``delimiter=','``
        """
        assert lexicon_csv_path is not None

        with open(lexicon_csv_path, encoding=encoding, newline='') as csv_file:
            lexicon_reader = csv.reader(csv_file, **csv_reader_keyword_arguments)
            for row in lexicon_reader:
                row = [item.strip() for item in row]
                try:
                    self._append_lexicon_entry_from_row(row)
                except ValueError as error:
                    raise csv.Error(
                        '%s:%d: %s' % (
                            lexicon_csv_path, lexicon_reader.line_num, error))

    def _append_lexicon_entry_from_row(self, original_row: List[str]):
        assert original_row is not None

        def enum_value_for(enum_type: Enum, name: str):
            """
            Enum entry matching lower case ``name`` in
            ``enum_type`` or ``None`` if ``name`` is empty.
            """
            assert enum_type is not None
            assert name is not None
            assert name.strip() == name

            if name == '':
                result = None
            else:
                enum_value_name = name.replace(' ', '_').upper()
                try:
                    result = enum_type[enum_value_name]
                except KeyError:
                    valid_names = sorted([enum_entry.name.lower() for enum_entry in enum_type])
                    raise ValueError('name %r for enum %s must be one of: %s'
                                     % (name, enum_type.__name__, valid_names))
            return result

        row = [item.strip() for item in original_row]
        row += 4 * ['']  # Ensure we have at least 4 strings
        lemma, _, topic_name, rating_name = row[:4]
        if lemma != '' and not lemma.startswith('#'):
            topic = enum_value_for(self._topic_enum, topic_name)
            rating = enum_value_for(self._rating_enum, rating_name)
            lexicon_entry = LexiconEntry(lemma, topic, rating)
            self.entries.append(lexicon_entry)

    def lexicon_entry_for(self, token: Token) -> LexiconEntry:
        """
        Entry in lexicon that best matches ``token``.
        """
        result = None
        lexicon_size = len(self.entries)
        lexicon_entry_index = 0
        best_matching = 0.0
        while lexicon_entry_index < lexicon_size and not tools.is_close(best_matching, 1.0):
            lexicon_entry = self.entries[lexicon_entry_index]
            matching = lexicon_entry.matching(token)
            if matching > best_matching:
                result = lexicon_entry
                best_matching = matching
            lexicon_entry_index += 1
        return result


class SentimentContext:
    def __init__(self, language: Union[Language, str], lexicon: Lexicon, synonyms: Dict[str, str]=None):
        assert language is not None
        if type(language) == str:
            self._language = spacy.load(language)
        else:
            self._language = language
        self._synonyms = {}
        if synonyms is not None:
            for from_text, to_text in synonyms:
                try:
                    from_regex = re.compile(r'\b' + from_text + r'\b')
                except re.error as error:
                    raise ValueError('cannot convert %r to regular expression: %s' % (from_text, error))
                self._synonyms[from_regex] = to_text

    @property
    def language(self) -> Language:
        return self._language

    @property
    def synonyms(self) -> Dict[Pattern, str]:
        return self._synonyms


def add_token_extension(force=False):
    """
    Extend spaCy's :py:class:`spacy.tokens.Token` with attributes for
    sentiment specific data.

    This should be called only once during the runtime of the application.
    If multiple calls cannot be avoided, use ``force=True`` to prevent spaCy
    from rejecting to redundant setting.
    """
    Token.set_extension('topic', default=None, force=force)
    Token.set_extension('rating', default=None, force=force)
    Token.set_extension('is_negation', default=False, force=force)
    Token.set_extension('is_intensifier', default=False, force=force)
    Token.set_extension('is_diminisher', default=False, force=force)


class OpinionMiner:
    """
    Miner for opinions written in a specific language based on a lexicon.

    Opinions are matched to a topic and :py:class:`Rating`.
    """
    def __init__(self, nlp: Language, lexicon: Lexicon, language_sentiment: LanguageSentiment, topic_type: Enum=None):
        assert nlp is not None
        assert lexicon is not None
        assert language_sentiment is not None
        self.nlp = nlp
        self.language_sentiment = language_sentiment
        self.lexicon = lexicon
        self._topic_type = topic_type
        self._emoticon_to_name_and_rating_map = create_emoticon_to_name_and_rating_map()
        self._idiom_to_localized_rating_text_map = compiled_idiom_to_localized_rating_text_map(
            language_sentiment.idioms, language_sentiment.rating_to_localized_text_map)

        def opinion_matcher(doc):
            """
            SpaCy pipeline pipe that sets opinion related attributes for each
            token.
            """
            for sentence in doc.sents:
                for token in sentence:
                    if self.language_sentiment.is_intensifier(token):
                        token._.is_intensifier = True
                    elif self.language_sentiment.is_diminisher(token):
                        token._.is_diminisher = True
                    elif self.language_sentiment.is_negation(token):
                        token._.is_negation = True
                    else:
                        lexicon_entry = self.lexicon.lexicon_entry_for(token)
                        if lexicon_entry is not None:
                            token._.rating = lexicon_entry.rating
                            token._.topic = lexicon_entry.topic
                        else:
                            # Check for lexicon independent negatives and positives.
                            lower_lemma = token.lemma_.lower()
                            rating = self.language_sentiment.negatives.get(lower_lemma)
                            if rating is None:
                                rating = self.language_sentiment.positives.get(lower_lemma)
                            if rating is not None:
                                token._.rating = rating
            return doc

        if self.nlp.has_pipe('opinion_matcher'):
            self.nlp.remove_pipe('opinion_matcher')
        self.nlp.add_pipe(opinion_matcher)

    def opinions(self, text: str) -> Generator[Tuple[Enum, Rating, List[Token]], None, None]:
        """
        Opinions found in ``text``. This yields an opinion for each sent in text.
        """
        assert text is not None

        _log.info('preprocessing text')
        document = self.nlp(self._preprocessed_text(text))
        for sent in document.sents:
            _log.info('analyzing: %s', str(sent).strip())
            topic, rating = self._topic_and_rating_of(sent)
            yield topic, rating, sent

    def _preprocessed_text(self, text: str) -> str:
        result = text
        result = replaced_idioms(text, self._idiom_to_localized_rating_text_map)
        return result

    def _topic_and_rating_of(self, tokens: List[Token]) -> Tuple[Enum, Rating]:
        assert tokens is not None

        result_topic = None
        result_rating = None
        opinion_essence = OpinionMiner._essential_tokens(tokens)
        self._combine_ratings(opinion_essence)
        for token in opinion_essence:
            _log.debug('  using token for opinion: %s', debugged_token(token))
            # print(debugged_token(token))
            if (token._.topic is not None) and (result_topic is None):
                result_topic = token._.topic
            if (token._.rating is not None) and (result_rating is None):
                result_rating = token._.rating
            if (result_topic is not None) and (result_rating is not None):
                break
        return result_topic, result_rating

    @staticmethod
    def _essential_tokens(tokens):
        return [token for token in tokens if OpinionMiner._is_essential(token)]

    @staticmethod
    def _is_essential(token: Token) -> bool:
        return token._.topic is not None \
               or token._.rating is not None \
               or token._.is_diminisher \
               or token._.is_intensifier \
               or token._.is_negation

    def _combine_ratings(self, tokens):
        # Find the first rating (if any).
        rating_token_index = next(
            (
                token_index for token_index in range(len(tokens))
                if tokens[token_index]._.rating is not None
            ),
            None  # Default if no rating token can be found
        )

        if rating_token_index is not None:
            # Apply modifiers to the left on the rating.
            original_rating_token = tokens[rating_token_index]
            combined_rating = original_rating_token._.rating
            combined_text = original_rating_token.text
            modifier_token_index = rating_token_index - 1
            modified = True  # Did the last iteration modify anything?
            while modified and modifier_token_index >= 0:
                modifier_token = tokens[modifier_token_index]
                if self.language_sentiment.is_intensifier(modifier_token):
                    combined_rating = self.language_sentiment.intensified(combined_rating)
                elif self.language_sentiment.is_diminisher(modifier_token):
                    combined_rating = self.language_sentiment.diminished(combined_rating)
                elif self.language_sentiment.is_negation(modifier_token):
                    combined_rating = negated_rating(combined_rating)
                else:
                    # We are done, no more modifiers
                    # to the left of this rating.
                    modified = False
                if modified:
                    # Discard the current modifier
                    # and move on to the token on the left.
                    combined_text = modifier_token.text + '+' + combined_text
                    del tokens[modifier_token_index]
                    modifier_token_index -= 1
                    _log.debug('  combining %s and %s to %s -> %s',
                               modifier_token, original_rating_token.text, combined_text, combined_rating.name)
            original_rating_token._.rating = combined_rating
