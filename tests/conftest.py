#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conftest.py for shapiro. For details, see https://pytest.org/latest/plugins.html.
"""
import os

import spacy
import spacy.language
from pytest import fixture

_PROJECT_FOLDER = os.path.dirname(os.path.dirname(__file__))
_DATA_FOLDER = os.path.join(_PROJECT_FOLDER, 'data')
_TESTS_FOLDER = os.path.dirname(__file__)


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
def restaurant_feedback_txt_path():
    return tests_data_path("restaurant_feedback.txt")


@fixture
def nlp_de() -> spacy.language.Language:
    return spacy.load('de')


@fixture
def nlp_en() -> spacy.language.Language:
    return spacy.load('en')
