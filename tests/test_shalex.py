"""
Tests for tools module.
"""
import spacy
from shapiro import shalex
from shapiro.analysis import Lexicon
from shapiro.common import RestaurantTopic
from spacy.language import Language


def test_lexicon_and_feedback_file(
        nlp_en: Language, en_restauranteering_csv_path: str, restaurant_feedback_txt_path: str):
    lexicon = Lexicon(RestaurantTopic)
    lexicon.read_from_csv(en_restauranteering_csv_path)

    with open(restaurant_feedback_txt_path, "r", encoding="utf-8") as restaurant_feedback_txt_file:
        feedback_text = restaurant_feedback_txt_file.read()

    nlp_en = spacy.load("en")

    document = nlp_en(feedback_text)
    for sentence in document.sents:
        shalex.unknown_lexicon_lemmas(lexicon, sentence)
