"""Test that src/style.py works correctly"""

import pytest

from tui.style import Style


def test_style_from_string():
    """Test that string is correctly converted to style"""
    style = Style.fromstr("rows=4, columns=7, inline=True")
    assert (style.area_info.rows == 4
            and style.area_info.columns == 7
            and style.compositor_info.inline is True)


def test_style_from_string_with_invalid_attribute():
    """Test that an exception is raised when an attribute which doesn't exist
    is passed"""
    with pytest.raises(ValueError):
        _ = Style.fromstr("random=6")


def test_style_from_string_with_invalid_value():
    """Test that an exception is raised when an invalid value is passed"""
    with pytest.raises(ValueError):
        _ = Style.fromstr("rows=rows")


def test_get_style_value():
    """Test that a style value is fetched correctly, given its attribute
    name"""
    style = Style.fromstr("rows=4, columns=7, inline=True")
    assert style.get_value("rows") == 4


def test_get_style_value_with_invalid_attribute():
    """Test that a style value is fetched correctly, given its attribute
    name"""
    style = Style.fromstr("rows=4, columns=7, inline=True")
    with pytest.raises(ValueError):
        style.get_value("random")
