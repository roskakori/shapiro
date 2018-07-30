===============
Developer guide
===============

The chapter describes how you can work with the source code and contribute to
it.


Getting the source code
=======================

This section describes how to get the source code and the relevant tools.

About git
---------

To obtain the source code you need `git <https://git-scm.com/>`_ and possibly
a GUI client like source tree. If you are working with macOS or Windows and do
not have a preferred GUI client yet, you might want to give
`SourceTree <https://www.sourcetreeapp.com/>`_ a try as it is comparably
simple to use and logically structured. Windows users might also want to take
a look at `TortoiseGit <https://tortoisegit.org/>`_ which extends the file
Explorer with icons and context menus to directly work with git.

The remainder of this chapter refers to git using command line calls. If you
are using a GUI client you will have to find the corresponding menu item in
it.


Checking out the source code
----------------------------

If you want to contribute, it is recommended that you fork the source code at
https://github.com/roskakori/shapiro then then checkout the fork:

1. Visit https://github.com and login. If you don't have an account already,
   first create one, it's free.

2. Visit https://github.com/roskakori/shapiro (the project repository)

3. Click on "Fork" (in the upper right part of the page). This creates a copy
   of the Shapiro project at your own account you can modify (and accidentally
   break) as much as you like without impacting the original project.

4. Clone your fork to your local disk, e.g. by running

.. code-block:: sh

    git clone https://github.com/my_user_name/shapiro.git

5. Once you have changes that might be useful to contribute, open a
   `pull request <https://help.github.com/articles/about-pull-requests/>`_
   so they can be merged into the original project repository.
6. If your fork becomes outdated and you want to apply the changes in the
   original project, you need to
   `sync the fork <https://help.github.com/articles/syncing-a-fork/>`_.
   Visit the link for details but normally this comes down to:

.. code-block:: sh

    cd .../shapiro  # Replace "..." by your local folder where the project folder is located
    git fetch upstream
    git checkout master
    git merge upstream/master

Text editors
------------

You should be able to modify the code with any text editor.

If you are using PyCharm as IDE, you have to mark the following folders as
"sources root":

* shapiro/src
* shapiro/tests

In order to do that, select the folder in the project panel (typically on the
left) and choose
:menuselection:`Project Context Menu --> Mark Directory as --> Sources Root`.


Working with the source code
============================

Building and testing
--------------------

To build the source code you need to install a few Python packages that help
with development. If you are using Anaconda, run:

.. code-block:: sh

    # Only of anaconda users
    conda install -c conda-forge pre_commit pyscaffold pytest-cov tox

After that you can run the test cases:

.. code-block:: sh

    python setup.py test

or simply:

.. code-block:: sh

    tox

When running ``tox`` the first time, it will setup a virtual Python
environment and consequently download and install all the required packages
and data. This might take a few minutes but will be much faster for
consecutive runs.


Pre commit hook
---------------

Shapiro includes a pre commit hook for git that attempts to help to keep the
code clean and simple to maintain while also detecting and preventing certain
kinds of common mistakes.

To activate it run:

.. code-block:: sh

    pre-commit install

When doing a commit for the first time, a few dependencies are installed which
might take few minutes. Eventually you should see an output similar to this
one:

.. code-block:: text

    [WARNING] Unstaged files detected.
    [INFO] Stashing unstaged files to .../.cache/pre-commit/patch1532945738.
    [INFO] Initializing environment for git://github.com/pre-commit/pre-commit-hooks.
    [INFO] Initializing environment for https://github.com/pre-commit/mirrors-isort.
    [INFO] Installing environment for git://github.com/pre-commit/pre-commit-hooks.
    [INFO] Once installed this environment will be reused.
    [INFO] This may take a few minutes...
    [INFO] Installing environment for https://github.com/pre-commit/mirrors-isort.
    [INFO] Once installed this environment will be reused.
    [INFO] This may take a few minutes...
    Trim Trailing Whitespace.................................................Passed
    Check for added large files..............................................Passed
    Check python ast.........................................................Passed
    Check JSON...........................................(no files to check)Skipped
    Check for merge conflicts................................................Passed
    Check Xml............................................(no files to check)Skipped
    Check Yaml...........................................(no files to check)Skipped
    Debug Statements (Python)................................................Passed
    Fix End of Files.........................................................Passed
    Fix requirements.txt.................................(no files to check)Skipped
    Mixed line ending........................................................Passed
    Flake8...................................................................Passed
    isort....................................................................Failed
    hookid: isort
    [INFO] Restored changes from .../.cache/pre-commit/patch1532945738.

Some minor mistakes are fixed automatically which will result in output like::

    Files were modified by this hook. Additional output:
    Fixing .../shapiro/src/shapiro/language.py

In case the pre commit hooks get in your way you can skip them for a single
commit using

.. code-block:: sh

    git commit --no-verify ...

or run

.. code-block:: sh

    pre-commit install

to disable it completely. However, it is recommended that you keep it
activated because in the end it is intended to make life easier for you and
other contributors.

If you have good reasons to think a pre commit rule is counter productive
please open an issue and suggest a better solution:

The same goes for suggestions to add further commit hooks. Plenty of them are
available from https://github.com/pre-commit/pre-commit-hooks.


Branching
---------

Currently all commit go to the master branch in order to keep the early phase
of the project simple and do not overburden possible contributors with the
excessive amount of usability fails in the abomination called "git".

However, there is already an issue to discuss more robust approaches in
`#26: Define branching guidelines <https://github.com/roskakori/shapiro/issues/26>`_.


.. _coding-guidelines:

Coding guidelines
=================

* Python source code should conform to the
  `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ guidelines. The maximum
  line length has been increased to 120 characters though because it's kind of
  pointless to have a 24+ inch screen and leave half of it empty.

  Luckily the project has a autopep8 pre-commit-hock so minor formatting errors
  are automatically fixed.

* Use natural naming, avoid abbreviations unless the save at least 4 letters
  and are common for the domain. For example, `pos` instead of "part of speech"
  is ok.

* Functions should either change something or return something but not both.
  This means that calling a function multiple times with the same parameters
  gives the same result each time.

  Valid exceptions from that are generator functions (obviously).


Documentation
=============

This section explains how Shapiro's documentation can be built, viewed and
modified. There are also a few guidelines on API documentation.

Build
-----

To build the documentation run:

.. code-block:: sh

    python setup.py docs

You can browse this local documentation by running

.. code-block:: sh

    open build/sphinx/html/index.html # macOS
    firefox build/sphinx/html/index.html # most Unix variants

or simply opening :file:`build/sphinx/html/index.html` in your preferred
browser.


Tools
-----

Shapiros documentation is written in `Sphinx <http://sphinx-doc.org/>`_. It is
formatted in `reStructuredText <http://sphinx-doc.org/rest.html>`__. Add
additional pages by creating rst-files in ``docs`` and adding them to the
`toctree <http://sphinx-doc.org/markup/toctree.html>`_ below. Use then
`references <http://sphinx-doc.org/markup/inline.html>`__ in order to link
them from this page, e.g. :ref:`authors <authors>` and :ref:`changes`.

It is also possible to refer to the documentation of other Python packages
with the
`Python domain syntax <http://sphinx-doc.org/domains.html#the-python-domain>`__.
You can reference the documentation of
`Sphinx <http://sphinx.pocoo.org>`__,
`Python <http://docs.python.org/>`__,
`NumPy <http://docs.scipy.org/doc/numpy>`__,
`SciPy <http://docs.scipy.org/doc/scipy/reference/>`__,
`matplotlib <http://matplotlib.sourceforge.net>`__,
`Pandas <http://pandas.pydata.org/pandas-docs/stable>`__,
`Scikit-Learn <http://scikit-learn.org/stable>`__. You can add more by
extending the ``intersphinx_mapping`` in your Sphinx's ``conf.py``.

The extension
`autodoc <http://www.sphinx-doc.org/en/stable/ext/autodoc.html>`__ is already
activated and lets you include documentation from docstrings. Technically,
Docstrings can be written in
`Google <http://google.github.io/styleguide/pyguide.html#Comments>`__,
`NumPy <https://numpydoc.readthedocs.io/en/latest/format.html>`__ and
`classical <http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists>`__
style.


Guidelines
----------

Avoid documentation in the source code as it tends to become outdated quickly
and rarely is maintained properly. Instead try to use these instead of
documentation:

* use meaningful names and clean code; see :ref:`coding-guidelines`
* type hints
* assertions

API documentation comments are useful at:

* The beginning of a module to give a general idea.
* The beginning of a class to give a general idea.
* Complex functions with multiple parameters.
* Functions with a high level of abstraction and no direct relation to real
  world constructs.
* Functions that are built on other peoples work, e.g. for providing links
  to algorithms or papers.

The preferred API documentation style is to use a concise explanation that
directly mentions parameters in it. Convoluted separate sections of parameters
and return values rarely add anything that type hints and assertions already
provide and just make the documentation harder to read.
