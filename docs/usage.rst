==========
User guide
==========


About sentiment analysis
========================

Definition
----------

TODO

Process
-------

1. Gather data
2. Preprocess raw data
3. Analyze cleaned up data
4. Interpret and act on results

TODO: elaborate

Challenges
----------

TODO

The lexicon
===========

Ratings
-------

TODO

Topics
------

TODO


The CSV format
--------------

TODO


Building the lexicon
====================

Collect the initial data
------------------------

TODO:

1. Obvious data source (e.g. menu, cook books, ...)
2. Use ``shapiro count`` on existing feedback and add the most common terms
3. Use ``shapiro lexicon --create / --append`` to add terms from existing feedback


Analyze data
------------

TODO: Use ``shapiro analyze`` to analyze specific feedback


The Language
============

TODO: explain:

1. sentiment words
2. intesifiers / diminishers
3. negators
4. modals
5. emojis
6. rules


Languages for shapiro
---------------------

Currently shapiro supports the following languages:

1. English
2. German

It should be possible to add other languages provided there is a
`spaCy language model <https://spacy.io/usage/models>`_ with support for
vocabulary, syntax and entities.

TODO: Explain how to add a language to :py:mod:`shapiro.language`.
