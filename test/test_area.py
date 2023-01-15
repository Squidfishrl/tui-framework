import pytest

from tui.area import Area
from tui.style import AreaInfo


@pytest.fixture
def five_rows_ten_columns_area():
    area_info = AreaInfo(min_rows=5, min_columns=10)
    area = Area(area_info=area_info)
    return area


@pytest.fixture
def three_by_three_area():
    area_info = AreaInfo(min_rows=3, min_columns=3)
    area = Area(area_info=area_info)
    return area


def test_area_init(five_rows_ten_columns_area: Area):
    """Test that an area is initialised correctly"""
    assert (len(five_rows_ten_columns_area.char_area) == 5 and
            len(five_rows_ten_columns_area.char_area[0]) == 10)


def test_area_ptr_movement(five_rows_ten_columns_area: Area):
    """Test that area_ptr movements are synchronised with char_area"""
    five_rows_ten_columns_area.area_ptr.column = 7
    five_rows_ten_columns_area.area_ptr.row = 2

    col = five_rows_ten_columns_area.area_ptr.column
    row = five_rows_ten_columns_area.area_ptr.row

    five_rows_ten_columns_area.char_area[row][col] = 'A'

    assert five_rows_ten_columns_area.char_area[2][7] == 'A'


def test_area_add_chars(five_rows_ten_columns_area: Area):
    """Test that adding a string without '\n' works correctly"""
    five_rows_ten_columns_area.area_ptr.column = 1
    five_rows_ten_columns_area.area_ptr.row = 2
    five_rows_ten_columns_area.add_chars("1234")

    assert (five_rows_ten_columns_area.char_area[2] == [' ', '1', '2', '3',
            '4', ' ', ' ', ' ', ' ', ' '])


def test_area_add_multiline_chars(three_by_three_area: Area):
    """Test that adding a string with '\n' works correctly"""
    three_by_three_area.area_ptr.column = 1
    three_by_three_area.area_ptr.row = 0
    three_by_three_area.add_chars("1\n2\n34")

    assert (three_by_three_area.char_area[0] == [' ', '1', ' '] and
            three_by_three_area.char_area[1] == ['2', ' ', ' '] and
            three_by_three_area.char_area[2] == ['3', '4', ' '])


def test_area_add_multiline_chars_with_column_preserve(
        three_by_three_area: Area):
    """Test that adding a string with '\n' with column presserve works
    correctly"""

    three_by_three_area.area_ptr.column = 1
    three_by_three_area.area_ptr.row = 0
    three_by_three_area.add_chars("1\n2\n34", column_preserve=True)

    assert (three_by_three_area.char_area[0] == [' ', '1', ' '] and
            three_by_three_area.char_area[1] == [' ', '2', ' '] and
            three_by_three_area.char_area[2] == [' ', '3', '4'])


def test_area_add_chars_invalid_size(three_by_three_area: Area):
    """Test that adding a string that exceeds size throws an IndexError"""
    three_by_three_area.area_ptr.column = 1
    three_by_three_area.area_ptr.row = 0
    with pytest.raises(IndexError):
        three_by_three_area.add_chars("123")


def test_area_add_multiline_chars_invalid_size(three_by_three_area: Area):
    """Test that adding a multiline string that exceeds size throws an
    IndexError"""
    three_by_three_area.area_ptr.column = 1
    three_by_three_area.area_ptr.row = 0
    with pytest.raises(IndexError):
        three_by_three_area.add_chars("12\n34\n1234")


def test_area_add_multiline_chars_with_column_preserve_invalid_size(
        three_by_three_area: Area):
    """Test that adding a multiline string with column preservation that
    exceeds size throws an IndexError"""
    three_by_three_area.area_ptr.column = 1
    three_by_three_area.area_ptr.row = 0
    with pytest.raises(IndexError):
        three_by_three_area.add_chars("12\n34\n123", column_preserve=True)


def test_area_to_string(three_by_three_area: Area):
    """Test that area is converted to string correctly"""
    three_by_three_area.add_chars("123\n456\n789")
    assert "123\n456\n789" == str(three_by_three_area)
