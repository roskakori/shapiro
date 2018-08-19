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


def test_can_analyze_restaurant_feedback_from_file(
        en_restauranteering_csv_path: str, en_restaurant_single_feedback_txt_path: str):
    assert 0 == process([
        'analyze', '--language=en', en_restauranteering_csv_path, en_restaurant_single_feedback_txt_path])


def test_can_analyze_immediate_restaurant_feedback(
        en_restauranteering_csv_path: str):
    assert 0 == process([
        'analyze', '--language=en', '--immediate', en_restauranteering_csv_path,
        'The', 'waiter', 'was', 'very', 'polite'])
