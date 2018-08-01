"""
The ``shapiro`` command line command.
"""
import argparse
import logging
import sys
from typing import Sequence

import spacy
from shapiro import __version__, analysis, tools
from spacy.language import Language

_DEFAULT_ENCODING = 'utf-8'
_DEFAULT_NUMBER_OF_LEMMAS_TO_PRINT = 20

_log = tools.log


def parsed_args(arguments: Sequence[str]):
    if arguments is None:  # pragma: no cover
        arguments = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='command line tool for lexicon based sentiment analysis')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(title='available commands')

    parser_count = subparsers.add_parser(
        'count', help='print most common lemmas and their count in a text file')
    tools.add_language_argument(parser_count)
    parser_count.add_argument(
        '--encoding', '-e', default=_DEFAULT_ENCODING,
        help='encoding of TEXT-FILE, default: %(default)s')
    parser_count.add_argument(
        '--number', '-n', type=int, default=_DEFAULT_NUMBER_OF_LEMMAS_TO_PRINT,
        help='number of most common lemmas to print, 0=all, default: %(default)s')
    parser_count.add_argument(
        '--pos', '-p', dest='use_pos', action='store_true',
        help='enable to include part of speech tag in output; '
             'consequently words might show multiple time, '
             'e.g. "pretty" as ADJ and ADV')
    parser_count.add_argument(
        '--stopwords', '-s', dest='count_stopwords', action='store_true',
        help='enable to also count stopwords')
    parser_count.add_argument(
        'text_to_analyze_path', metavar='TEXT-FILE')
    parser_count.set_defaults(func=command_count)

    result = parser.parse_args(arguments)
    if 'func' not in result:
        parser.error('COMMAND must be specified')

    return result


def command_count(args: argparse.Namespace):
    nlp = _nlp(args)
    number = args.number
    count_stopwords = args.count_stopwords
    use_pos = args.use_pos
    with open(args.text_to_analyze_path, encoding=args.encoding) as text_file:
        most_common_lemmas = analysis.most_common_lemmas(
            nlp, text_file,
            number=number, count_stopwords=count_stopwords, use_pos=use_pos)
        for count, lemma, pos in most_common_lemmas:
            row_to_write = [str(count), lemma]
            if use_pos:
                row_to_write.append(str(pos))
            print('\t'.join(row_to_write))


def _nlp(args: argparse.Namespace) -> Language:
    _log.info('loading language "%s"', args.language)
    return spacy.load(args.language)


def process(arguments: Sequence[str]=None):
    result = 1
    try:
        args = parsed_args(arguments)
        args.func(args)
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