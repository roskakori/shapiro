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

.. index::
    single: lexicon

The lexicon
===========

.. index::
    single: rating

Ratings
-------

TODO
.. index::
    single: topic

Topics
------

TODO

.. index::
    single: POS; part-of-speech; tagging

Part-of-speech
--------------

`Part-of-speech <https://en.wikipedia.org/wiki/Part_of_speech>`_ (POS)
describes a category of words that have similar grammatical properties.

The categories available with spaCy depend on the language are described in
spaCy's `documentation on part-of-speech tagging <https://spacy.io/api/annotation#pos-tagging>`_.
A few common cetegories available in many languages are:

* adj (adjective), for example "quick"
* adv (adverb) for example "quickly"
* conj (conjunction) for example "and" or "but"
* det (determiner) for example "the"
* "intj" (interjection) for example "hello"
* noun for example "car"
* num (number) for example "123" and "billion"
* propn (proper noun) for example "Alice", "Vienna" or "EU"
* punct (punctuation), for example "." and "!"
* sym (symbol) for example "€"
* verb, for example "drive"


.. index::
    single: CSV

The CSV format
--------------

Shapiro's command line tools use CSV files to exchange and store lexicons.
CSV stands for "comma separated values" where text files can be used to store
tabular data separated by comma (","). There are also escape mechanisms to
store commas, line breaks and quotes. Refer to
`RFC-4180 <https://tools.ietf.org/html/rfc4180>`_ for more details.

While CSV is simple and widely used, it sadly does not provide a way to
specify certain file properties from the outside, so shapiro assumes them:

* Delimiter: comma (,)
* Quote character: double quote (")
* Encoding: `UTF-8 <https://en.wikipedia.org/wiki/UTF-8>`_ (without an initial
  UTF-8 BOM)

While it is possible to edit CSV files with a text editor, this is cumbersome
and error prone. Instead you can also use a spread sheet application such as
`LibreOffice Calc <https://www.libreoffice.org/>`_ or to some extend
`Microsoft Excel <https://products.office.com/en/excel>`_ though the latter
has a tendency to produce different files depending on your regional settings
and thus might be unable to easily produce CSV files that shapiro can process.


Building the lexicon
====================

Collect the initial data
------------------------

Domain specific documents
~~~~~~~~~~~~~~~~~~~~~~~~~

Your first source for lemmas to add to the lexicon might be obvious words you
can collect from existing documents from your domain. For example
restauranteering uses many words around food and beverages that can be
collected from the restaurant's menu or from lists of ingredients.

.. index::
    pair: shapiro; count

Most common words derived with ``shapiro count``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``shapiro count`` command can read text files, extract and count the
lemmas found in it and print the most common ones.

For example:

.. code-block:: sh

    shapiro count --language en data/en_restauranteering_data.csv

The output could look like:

.. code-block:: text

    7	place
    7	food
    6	good
    4	restaurant
    3	service
    3	price
    3	atmosphere

To see a full list of available options use:

.. code-block:: sh

    shapiro --help count


.. index::
    pair: shapiro; lexicon

Maintain a lexicon with ``shapiro lexicon``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Use ``shapiro lexicon --create / --append`` to add terms from existing feedback


.. index::
    pair: shapiro; analyze

Analyze data
------------

TODO: Use ``shapiro analyze`` to analyze specific feedback


The Language
============

TODO: explain:

1. sentiment words
2. intensifiers / diminishers
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
