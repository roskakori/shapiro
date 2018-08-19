"""
The ``shapiro`` command line command.
"""
import argparse
import logging
import sys
from typing import Sequence

import spacy
from shapiro import __version__, analysis, tools
from shapiro.common import Rating, RestaurantTopic
from shapiro.language import language_sentiment_for
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

    parser_analyze = subparsers.add_parser(
        'analyze', help='extract opinions from a text')
    _add_debug_argument(parser_analyze)
    parser_analyze.add_argument(
        '--encoding', '-e', default=_DEFAULT_ENCODING,
        help='encoding of TEXT-FILE, default: %(default)s')
    _add_language_argument(parser_analyze)
    parser_analyze.add_argument(
        '--immediately', '-i', action='store_true',
        help='interpret TEXT-FILE as immediate text instead of path to file')
    parser_analyze.add_argument(
        'lexicon_csv_path', metavar='LEXICON-FILE',
        help='CSV file with lexicon to use for analysis')
    parser_analyze.add_argument(
        'text_to_analyze_paths', metavar='TEXT-FILE', nargs='+', help='text file(s) to analyze')
    parser_analyze.set_defaults(func=command_analyze)

    parser_count = subparsers.add_parser(
        'count', help='print most common lemmas and their count in a text file')
    _add_language_argument(parser_count)
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


def _add_debug_argument(parser: argparse.ArgumentParser):
    """
    Add ``--debug`` to an :class:`argparse.ArgumentParser` enables debug logging.
    """
    parser.add_argument('--debug', '-D', action='store_true', help='enable debug logging')


def _add_language_argument(parser: argparse.ArgumentParser):
    """
    Add ``--language`` to an :class:`argparse.ArgumentParser` that refers to a
    2 letter `ISO-639-1 language code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_
    for witch spacy must provide a matching :class:`spacy.language.Language`.
    """
    parser.add_argument('--language', '-l', default='en',
                        help='two letter ISO-639-1 language code for spaCy; default: %(default)s')


def _possibly_enable_debug_logging(args: argparse.Namespace):
    if args.debug:
        _log.setLevel(logging.DEBUG)


def command_analyze(args: argparse.Namespace):
    def analyze(text: str):
        for topic, rating, sent in opinion_miner.opinions(text):
            topic_text = topic.name.lower() if topic is not None else ''
            rating_text = rating.name.lower() if rating is not None else ''
            sent_text = str(sent).strip()
            # TODO: Use proper csv.writer() instead of hacked together escaping.
            csv_escaped_sent_text = '"' + sent_text.replace('"', '""') + '"'
            print(f'{topic_text},{rating_text},{csv_escaped_sent_text}')

    nlp = _nlp(args)
    # FIXME: Use generic topics instead of hard coded RestaurantTopic.
    lexicon = analysis.Lexicon(RestaurantTopic, Rating)
    lexicon.read_from_csv(args.lexicon_csv_path, encoding=args.encoding)
    language_sentiment = language_sentiment_for(args.language)
    opinion_miner = analysis.OpinionMiner(nlp, lexicon, language_sentiment)
    _possibly_enable_debug_logging(args)

    print('# topic,rating,text')
    text_to_analyze_paths = args.text_to_analyze_paths
    if args.immediately:
        text = ' '.join(text_to_analyze_paths)
        analyze(text)
    else:
        for text_to_analyze_path in text_to_analyze_paths:
            _log.info('reading text to analyze from "%s"', text_to_analyze_path)
            with open(text_to_analyze_path, 'r', encoding=args.encoding) as text_to_analyze_file:
                # NOTE: Memory wise it would generally be nicer to read the text line by line.
                # However we cannot ensure that the end of a line also constitutes the end of
                # a sentence, so we need to read the whole text and pass it to spaCy to split
                # into sentences.
                text = text_to_analyze_file.read()
                analyze(text)


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


def command_lexicon(args: argparse.Namespace):
    raise NotImplementedError('lexicon')


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
    analysis.add_token_extension()
    sys.exit(process())


if __name__ == '__main__':  # pragma: no cover
    main()
