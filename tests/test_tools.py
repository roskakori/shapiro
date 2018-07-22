"""
Tests for tools module.
"""
from shapiro import tools


def test_can_detect_close_float_numbers():
    assert tools.is_close(0.0, 0.0)
    assert tools.is_close(1.0, 1.0)
    assert not tools.is_close(1.0, 0.99)
