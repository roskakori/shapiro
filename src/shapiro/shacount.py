"""
Read a text file and print the most common lemmas in it.
"""
import argparse
import logging
import sys
from typing import Sequence

import spacy
from spacy.language import Language

from shapiro import analysis
from shapiro import tools


_DEFAULT_NUMBER_OF_LEMMAS_TO_PRINT = 20

_log = tools.log


def parsed_args(arguments: Sequence[str]) -> argparse.Namespace:
    if arguments is None:  # pragma: no cover
        arguments = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    tools.add_language_argument(parser)
    parser.add_argument('--number', '-n', type=int, default=_DEFAULT_NUMBER_OF_LEMMAS_TO_PRINT,
                        help='number of most common lemmas to print, 0=all, default: %(default)s')
    parser.add_argument('--pos', '-p', dest='use_pos', action='store_true',
                        help='enable to include part of speech tag in output; '
                             'consequently words might show multiple time, '
                             'e.g. "pretty" as ADJ and ADV')
    parser.add_argument('--stopwords', '-s', dest='count_stopwords', action='store_true',
                        help='enable to also count stopwords?')
    parser.add_argument('text_to_analyze_path', metavar='TEXT-FILE')
    tools.add_version_argument(parser)
    return parser.parse_args(arguments)


def shacount(nlp: Language, text_path: str, encoding='utf-8',
             number: int=_DEFAULT_NUMBER_OF_LEMMAS_TO_PRINT, count_stopwords: bool=False, use_pos: bool=False):
    _log.info('read and tokenize "%s"', text_path)
    with open(text_path, encoding=encoding) as text_file:
        for count, lemma, pos in analysis.most_common_lemmas(nlp, text_file, number=number, count_stopwords=count_stopwords, use_pos=use_pos):
            row_to_write = [str(count), lemma]
            if use_pos:
                row_to_write.append(str(pos))
            print('\t'.join(row_to_write))


def process(arguments: Sequence[str]=None):
    result = 1
    try:
        args = parsed_args(arguments)
        _log.info('loading language "%s"', args.language)
        nlp = spacy.load(args.language)
        shacount(
            nlp, args.text_to_analyze_path,
            number=args.number, count_stopwords=args.count_stopwords, use_pos=args.use_pos)
        result = 0
    except KeyboardInterrupt:  # pragma: no cover
        _log.error('interrupted as requested by user')
    except OSError as error:
        _log.error(error)
    except Exception as error:
        _log.exception(error)

    return result


def main():  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    sys.exit(process())


if __name__ == '__main__':  # pragma: no cover
    main()
