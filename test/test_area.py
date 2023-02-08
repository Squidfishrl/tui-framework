"""Test that ./src/area.py is behaving correctly"""

import pytest

from tui.area import Area
from tui.style import AreaInfo
from tui.styles.border import DefaultBorder


@pytest.fixture
def five_rows_ten_columns_area():
    """Return an area with five rows and ten columns"""
    area_info = AreaInfo(rows=5, columns=10)
    area = Area(area_info=area_info)
    return area


@pytest.fixture
def three_by_three_area():
    """Return an area with three rows and three columns"""
    area_info = AreaInfo(rows=3, columns=3)
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


def test_area_add_minimal_border(three_by_three_area: Area):
    """Test that smallest possible area border is applied corectly"""
    three_by_three_area.add_border(border=DefaultBorder)
    assert str(three_by_three_area) == """\
╔═╗
║ ║
╚═╝\
"""


def test_area_with_minimal_border_add_char(three_by_three_area: Area):
    """Test that text inside the smallest possible area border is applied
    corectly"""
    three_by_three_area.add_border(border=DefaultBorder)
    three_by_three_area.add_chars(string="x")
    assert str(three_by_three_area) == """\
╔═╗
║x║
╚═╝\
"""


def test_area_with_minimal_border_add_char_with_invalid_size(
        three_by_three_area: Area
):
    """Test that adding text which would fit without having a border and
    wouldn't fit when having a border throws an IndexError when there's a
    border"""
    three_by_three_area.add_border(border=DefaultBorder)
    with pytest.raises(IndexError):
        three_by_three_area.add_chars(string="xx")


def test_area_add_border(five_rows_ten_columns_area: Area):
    """Test that area border is applied corectly"""
    five_rows_ten_columns_area.add_border(border=DefaultBorder)
    assert str(five_rows_ten_columns_area) == """\
╔════════╗
║        ║
║        ║
║        ║
╚════════╝\
"""


def test_minimal_area_with_margin_add_border():
    """Test that border is applied correctly to an area which has margin.
    Area has no excess space
    """
    five_by_five_area = Area(area_info=AreaInfo(
            rows=5,
            columns=5,
            margin_bottom=1,
            margin_right=1,
            margin_left=1,
            margin_top=1
        ))
    five_by_five_area.add_border(border=DefaultBorder)
    assert str(five_by_five_area) == """\
     
 ╔═╗ 
 ║ ║ 
 ╚═╝ 
     \
"""


def test_area_with_margin_add_border():
    """Test that border is applied correctly to an area which has margin."""
    five_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=5,
            columns=10,
            margin_bottom=2,
            margin_right=1,
            margin_left=2,
            margin_top=0
        ))
    five_rows_ten_columns_area.add_border(border=DefaultBorder)
    assert str(five_rows_ten_columns_area) == """\
  ╔═════╗ 
  ║     ║ 
  ╚═════╝ 
          
          \
"""


def test_area_with_margin_with_border_add_char():
    """Test that string is added correctly to an area which has margin and
    border"""
    five_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=5,
            columns=10,
            margin_bottom=2,
            margin_right=1,
            margin_left=2,
            margin_top=0
        ))
    five_rows_ten_columns_area.add_border(border=DefaultBorder)
    five_rows_ten_columns_area.add_chars("12345")
    assert str(five_rows_ten_columns_area) == """\
  ╔═════╗ 
  ║12345║ 
  ╚═════╝ 
          
          \
"""


def test_area_with_margin_with_border_add_char_with_invalid_size():
    """Test that an area which has margin and border throws an exception when
    an invalid string is added"""
    five_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=5,
            columns=10,
            margin_bottom=2,
            margin_right=1,
            margin_left=2,
            margin_top=0
        ))
    five_rows_ten_columns_area.add_border(border=DefaultBorder)
    with pytest.raises(IndexError):
        five_rows_ten_columns_area.add_chars("12345\n6")


def test_area_with_border_and_invalid_padding():
    """Test that border which would normally be allowed in area raises an
    exception when there's existing padding that takes all the space"""
    three_by_three_area = Area(area_info=AreaInfo(
            rows=3,
            columns=3,
            padding_bottom=1,
            padding_left=1,
            padding_right=1,
            padding_top=1
        ))

    with pytest.raises(IndexError):
        three_by_three_area.add_border(border=DefaultBorder)
    assert True


def test_area_with_border_with_padding_add_char():
    """Test that add_char works correctly when there's an area with a border
    and padding"""
    five_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=5,
            columns=10,
            padding_bottom=1,
            padding_right=1,
            padding_left=1,
            padding_top=1
        ))
    five_rows_ten_columns_area.add_border(border=DefaultBorder)
    five_rows_ten_columns_area.add_chars("012345")
    assert str(five_rows_ten_columns_area) == """\
╔════════╗
║        ║
║ 012345 ║
║        ║
╚════════╝\
"""


def test_area_with_border_with_padding_add_char_with_invalid_size():
    """Test that add_char with invalid size raises an exception when there's
    an area with a border and padding"""
    five_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=5,
            columns=10,
            padding_bottom=1,
            padding_right=1,
            padding_left=1,
            padding_top=1
        ))
    five_rows_ten_columns_area.add_border(border=DefaultBorder)
    with pytest.raises(IndexError):
        five_rows_ten_columns_area.add_chars("0123456")


def test_area_with_margin_with_border_with_padding_add_char():
    """Test that add_char works correctly when there's an area utilizes the
    entire box model (margin, border, padding)"""
    seven_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=7,
            columns=10,
            margin_bottom=1,
            margin_left=1,
            margin_right=1,
            margin_top=1,
            padding_bottom=1,
            padding_right=1,
            padding_left=1,
            padding_top=1
        ))
    seven_rows_ten_columns_area.add_border(border=DefaultBorder)
    seven_rows_ten_columns_area.add_chars("0123")
    assert str(seven_rows_ten_columns_area) == """\
          
 ╔══════╗ 
 ║      ║ 
 ║ 0123 ║ 
 ║      ║ 
 ╚══════╝ 
          \
"""


def test_area_with_margin_with_border_with_padding_add_char_invalid_size():
    """Test that add_char with invalid size raises an exception when there's an
    area utilizes the entire box model (margin, border, padding)"""
    seven_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=7,
            columns=10,
            margin_bottom=1,
            margin_left=1,
            margin_right=1,
            margin_top=1,
            padding_bottom=1,
            padding_right=1,
            padding_left=1,
            padding_top=1
        ))
    seven_rows_ten_columns_area.add_border(border=DefaultBorder)
    with pytest.raises(IndexError):
        seven_rows_ten_columns_area.add_chars("01234")


def test_area_with_margin_with_padding_add_char():
    """Test that add_char works correctly when there's an area with margin and
    padding"""
    seven_rows_ten_columns_area = Area(area_info=AreaInfo(
            rows=7,
            columns=10,
            margin_bottom=1,
            margin_left=1,
            margin_right=1,
            margin_top=1,
            padding_bottom=1,
            padding_right=1,
            padding_left=1,
            padding_top=1
        ))
    seven_rows_ten_columns_area.add_chars("012345")
    assert str(seven_rows_ten_columns_area) == """\
          
          
  012345  
          
          
          
          \
"""
