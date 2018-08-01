"""
Tests for :py:mod:`shapiro.commandline`.
"""
import pytest
from shapiro.commandline import process


def test_can_print_help():
    with pytest.raises(SystemExit) as exception_info:
        process(['--help'])
    assert exception_info.value.code == 0


def test_can_print_version():
    with pytest.raises(SystemExit) as exception_info:
        process(['--version'])
    assert exception_info.value.code == 0


def test_fails_on_missing_command():
    with pytest.raises(SystemExit) as exception_info:
        process([])
    assert exception_info.value.code == 2


def test_fails_on_unknown_command():
    with pytest.raises(SystemExit) as exception_info:
        process(['unknown_command'])
    assert exception_info.value.code == 2


def test_can_count_restaurant_feedback(restaurant_feedback_txt_path: str):
    assert 0 == process(['count', restaurant_feedback_txt_path])
    assert 0 == process(['count', '--pos', restaurant_feedback_txt_path])
    assert 0 == process(['count', '--stopwords', restaurant_feedback_txt_path])
