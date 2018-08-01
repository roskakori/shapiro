#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conftest.py for shapiro. For details, see https://pytest.org/latest/plugins.html.
"""
import os

import spacy
import spacy.language
from pytest import fixture
from shapiro.analysis import Lexicon, add_token_extension
from shapiro.common import RestaurantTopic
from shapiro.language import EnglishSentiment, GermanSentiment

_PROJECT_FOLDER = os.path.dirname(os.path.dirname(__file__))
_DATA_FOLDER = os.path.join(_PROJECT_FOLDER, 'data')
_TESTS_FOLDER = os.path.dirname(__file__)


@fixture(scope="session", autouse=True)
def execute_before_any_test():
    """
    One time initialization needed by all tests.
    """
    add_token_extension()


def data_path(name: str) -> str:
    """
    Folder where example data to read are located.
    """
    assert name is not None
    return os.path.join(_DATA_FOLDER, name)


def tests_path(name: str) -> str:
    """
    Folder where test data to read are located.
    """
    assert name is not None
    return os.path.join(_TESTS_FOLDER, name)


def tests_data_path(name: str) -> str:
    """
    Folder where test data to read are located.
    """
    assert name is not None
    return os.path.join(_TESTS_FOLDER, 'data', name)


@fixture
def en_restauranteering_csv_path():
    return data_path('en_restauranteering.csv')


@fixture
def en_restaurant_single_feedback_txt_path():
    return data_path('en_restaurant_single_feedback.txt')


@fixture
def restaurant_feedback_txt_path():
    return tests_data_path("restaurant_feedback.txt")


@fixture
def nlp_de() -> spacy.language.Language:
    return spacy.load('de')


@fixture
def nlp_en() -> spacy.language.Language:
    return spacy.load('en')


@fixture
def english_sentiment() -> EnglishSentiment:
    return EnglishSentiment()


@fixture
def german_sentiment() -> GermanSentiment:
    return GermanSentiment()


@fixture
def lexicon_restauranteering() -> Lexicon:
    result = Lexicon(RestaurantTopic)
    result.read_from_csv(en_restauranteering_csv_path())
    return result
