=======
shapiro
=======


Lexicon based sentiment analysis.


Overview
========

Shapiro provides building blocks for sentiment analysis. The current
implementation is a improved variant of code examples from a talk about
`Introduction to sentiment analysis with spaCy <https://github.com/roskakori/talks/blob/master/europython/sentiment_analysis/introduction_to_sentiment_analysis.ipynb>`_
I gave at the `EuroPython 2018 <https://ep2018.europython.eu)>`_ conference.

Shapiro's goals are:

* provide functions for common preprocessing tasks like replacing synonyms
  and unifying emojis/smiley codes
* provide means to read a sentiment lexicon and match tokens with it
* provide ways to model domain independent sentiment specific parts of Latin
  based languages (like negators and intensifiers)
* provide means to assign sentiment information to idioms
* (long term) provide ways to model a grammar for more advanced sentiment
  analysis similar to the one described Bing Liu (2015) "Sentiment Analysis:
  Mining Opinions, Sentiments, and Emotions".

Currently it provides basic support for:

* Users can provide lexicons (in CSV format) to assign topics and ratings to
  sentiment words
* Negators, intensifiers and diminishers (and combinations of them). Currently
  there is support for English and German. Adding more languages based on Latin
  should be possible.
* Lemmatization, part of speech tagging and basic language modelling by using
  `spaCy <https://spacy.io>`_.

This is a work in progress and features might be added and changed as seem
fit. So the API is a moving target.


Getting started
===============

To use shapiro, you need Python and spaCy. The easiest way to get it is:

1. Download and install anaconda from https://www.anaconda.com/download/
2. Install spaCy::

    conda install -c conda-forge spacy

3. Install Tox::

    conda install -c conda-forge tox

4. Download the language models you need. For example to get English and
   German run::

    python -m spacy download en
    python -m spacy download de

For more information on installing spaCy visit https://spacy.io/usage/. For
details on available free language models visit https://spacy.io/usage/models.
