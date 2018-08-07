#!/bin/bash
# Shell script for local jenkins build.

# Fail script after first error.
set -e

# Setup the Python environment.
python3 -m venv .jenkins_env_shapiro
source .jenkins_env_shapiro/bin/activate
pip3 install --upgrade pip
pip3 install --upgrade wheel

# Measure size of project
pip3 install --upgrade pygount
pygount --format=cloc-xml --out=cloc.xml

# Check coding guidelines.
# TODO: Reactivate: tox -e flake8

# Run tests.
#
# HACK: We should be able to do this with "tox" but for some reason it does
# not write coverage data.
python3 setup.py test

deactivate
