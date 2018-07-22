"""
Types and functions for sentiment analysis.
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

_log = tools.log


class Rating(Enum):
    VERY_BAD = -3
    BAD = -2
    SOMEWHAT_BAD = -1
    UNKNOWN = 0
    SOMEWHAT_GOOD = 1
    GOOD = 2
    VERY_GOOD = 3


class LexiconEntry:
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
        result = 'LexiconEntry(%s, word_type=%s' % (self.lemma, self.word_type.name)
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
    def __init__(self, topics: Enum, ratings: Enum):
        assert topics is not None
        assert ratings is not None

        def name_to_enum_map(enum_type: Enum) -> Dict[str, Any]:
            result = {}
            for enum_entry in enum_type:
                enum_name = enum_entry.name.lower()
                if enum_name in result:
                    raise ValueError('case insensitive name %r for enum %s must be unique'
                                     % (enum_name, enum_type.__name__))
                result[enum_name] = enum_entry
            return result

        # Build maps to map texts from CSV to topic and rating.
        self.entries: List[LexiconEntry] = []
        self._topics = topics
        self._ratings = ratings
        self._topic_name_to_topic_map = name_to_enum_map(topics)
        self._rating_name_to_rating_map = name_to_enum_map(ratings)

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
                row += 3 * ['']  # Ensure we have at least 4 strings
                try:
                    self._append_lexicon_entry_from_row(row)
                except ValueError as error:
                    raise csv.Error(
                        '%s:%d: %s' % (
                            lexicon_csv_path, lexicon_reader.line_num, error))

    def _append_lexicon_entry_from_row(self, original_row: List[str]):
        assert original_row is not None

        def enum_value_for(name_to_enum_entry_map: Dict[str, Any], name: str):
            """
            Enum entry matching lower case ``name`` in
            ``name_to_enum_entry_map`` or ``None`` if ``name`` is empty.
            """
            assert name_to_enum_entry_map is not None
            assert len(name_to_enum_entry_map) >= 1
            assert name is not None
            assert name.strip() == name

            if name == '':
                result = None
            else:
                try:
                    result = name_to_enum_entry_map[name.lower()]
                except KeyError:
                    enum_type = type(next(iter(name_to_enum_entry_map.values())))
                    valid_names = sorted(name_to_enum_entry_map.keys())
                    raise ValueError('name %r for enum %s must be one of: %s'
                                     % (name, enum_type.__name__, valid_names))
            return result

        row = [item.strip() for item in original_row]
        row += 3 * ['']  # Ensure we have at least 3 strings
        lemma, topic_name, rating_name = row[:3]
        if lemma != '' and not lemma.startswith('#'):
            topic = enum_value_for(self._topic_name_to_topic_map, topic_name)
            rating = enum_value_for(self._rating_name_to_rating_map, rating_name)
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


def compiled_synonym_source_to_target_map(synonym_source_to_target_map: Dict[str, str]) -> Dict[Pattern, str]:
    result = {}
    if synonym_source_to_target_map is not None:
        for source_text, target_text in synonym_source_to_target_map.items():
            try:
                source_regex = re.compile(r'\b' + source_text + r'\b')
            except re.error as error:
                raise ValueError('cannot convert %r to regular expression: %s' % (source_text, error))
            result[source_regex] = target_text
    return result


def replaced_synonyms(sentence: str, synonym_source_pattern_to_target_map: Dict[Pattern, str]) -> str:
    assert sentence is not None
    assert synonym_source_pattern_to_target_map is not None
    result = sentence
    is_debug = _log.isEnabledFor(logging.DEBUG)
    for source_word_pattern, target_word in synonym_source_pattern_to_target_map.items():
        possible_modified_sentence = source_word_pattern.sub(target_word, result)
        if possible_modified_sentence != result:
            if is_debug:
                _log.debug('replaced synonym %s by %r', source_word_pattern.pattern, target_word)
            result = possible_modified_sentence
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
