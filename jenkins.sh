#!/bin/bash
# Shell script for local jenkins build.

# Fail script after first error.
set -e

# Setup the Python environment.
python3 -m venv .jenkins_env_shapiro
source .jenkins_env_shapiro/bin/activate
pip install --upgrade pip
pip install --upgrade wheel

# Measure size of project
pip install --upgrade pygount
pygount --format=cloc-xml --out=cloc.xml

# Check coding guidelines.
tox -e flake8

# Run tests.
#
# HACK: We should be able to do this with "tox" but for some reason it does
# not write coverage data.
python3 setup.py test

deactivate
