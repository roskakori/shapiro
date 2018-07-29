"""
Show lemmas found in a text file that are not already part of a lexicon.
"""
import argparse
import logging
import sys
from typing import List

import spacy
from spacy.tokens import Token

from shapiro import tools
from shapiro.analysis import Lexicon, LexiconEntry
from shapiro.common import RestaurantTopic

_log = tools.log


def _parsed_args(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__.strip()
    )
    parser.add_argument(
        "lexicon_path", metavar="LEXICON", help="existing lexicon file"
    )
    parser.add_argument(
        "text_path", metavar="TEXT", help="text file"
    )
    parser.add_argument(
        "--version", action="version", version="TODO"
    )
    return parser.parse_args(arguments)


def process(arguments=None):
    result = 1
    try:
        arguments = _parsed_args(arguments)
        print(arguments.lexicon_path)
        unknown_lexicon_lemma_from(arguments.lexicon_path, arguments.text_path)
        result = 0
    except KeyboardInterrupt:  # pragma: no cover
        _log.error('interrupted as requested by user')
    except OSError as error:
        _log.error(error)
    except Exception as error:
        _log.exception(error)

    return result


def unknown_lexicon_lemma_from(en_restauranteering_csv_path: str, restaurant_feedback_txt_path: str):
    # shalex.process([en_restauranteering_csv_path, restaurant_feedback_txt_path])
    lexicon = Lexicon(RestaurantTopic)
    lexicon.read_from_csv(en_restauranteering_csv_path)

    with open(restaurant_feedback_txt_path, "r", encoding="utf-8") as restaurant_feedback_txt_file:
        feedback_text = restaurant_feedback_txt_file.read()

    nlp_en = spacy.load("en")

    document = nlp_en(feedback_text)
    for sentence in document.sents:
        yield from unknown_lexicon_lemmas(lexicon, sentence)


def unknown_lexicon_lemmas(lexicon: Lexicon, tokens: List[Token]):

    for token in tokens:
        if lexicon.lexicon_entry_for(token) is None:
            yield token.lemma_


def main():  # pragma: no cover
    logging.basicConfig(level=logging.WARNING)
    sys.exit(process())


if __name__ == '__main__':  # pragma: no cover
    main()
