#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conftest.py for shapiro. For details, see https://pytest.org/latest/plugins.html.
"""
import os

import spacy
import spacy.language
from pytest import fixture


_TEST_DATA_FOLDER = os.path.dirname(__file__)


def test_data_path(name: str) -> str:
    """
    Folder where test data to read are located."
    """
    assert name is not None
    return os.path.join(_TEST_DATA_FOLDER, name)


@fixture
def en_restauranteering_csv_path():
    return test_data_path('en_restauranteering.csv')


@fixture
def nlp_en() -> spacy.language.Language:
    return spacy.load('en')
