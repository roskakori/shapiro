"""
Tests for tools module.
"""
from enum import Enum

from shapiro import shalex
from shapiro.analysis import Lexicon
import spacy


class _Topic(Enum):
    GENERAL, FOOD, HYGIENE, SERVICE, VALUE = range(5)


def test_lexicon_and_feedback_file(en_restauranteering_csv_path: str, restaurant_feedback_txt_path: str):
    # shalex.process([en_restauranteering_csv_path, restaurant_feedback_txt_path])
    lexicon = Lexicon(_Topic)
    lexicon.read_from_csv(en_restauranteering_csv_path)

    with open(restaurant_feedback_txt_path, "r", encoding="utf-8") as restaurant_feedback_txt_file:
        feedback_text = restaurant_feedback_txt_file.read()

    nlp_en = spacy.load("en")

    document = nlp_en(feedback_text)
    for sentence in document.sents:
        shalex.unknown_lexicon_lemmas(lexicon, sentence)
