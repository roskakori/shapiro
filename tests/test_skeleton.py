#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from shapiro.skeleton import fib

__author__ = "Thomas Aglassinger"
__copyright__ = "Thomas Aglassinger"
__license__ = "lgpl3"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
