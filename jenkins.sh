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

# Run tox tests.
tox
deactivate
