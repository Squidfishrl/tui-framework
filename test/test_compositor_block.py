"""Test that src/compositor.py block compositing works correctly"""
import pytest

from tui.compositor import Compositor, InsufficientAreaError
from tui.components.division import Division
from tui.style import Style
from tui.styles.area import AreaInfo


@pytest.fixture
def ten_by_ten_div():
    """Return a division with 10 rows and 10 columns"""
    style = Style(area_info=AreaInfo(columns=10, rows=10))
    return Division(identifier="div1", style=style)


@pytest.fixture
def ten_by_three_divs():
    """Return a division with three rows and ten columns"""
    style = Style(area_info=AreaInfo(columns=10, rows=3))
    divs = []

    for identifier in range(4):
        divs.append(Division(identifier=str(identifier), style=style))

    return divs


@pytest.fixture
def ten_by_one_divs():
    """Return a division with one row and ten columns"""
    style = Style(area_info=AreaInfo(columns=10, rows=1))
    divs = []

    for identifier in range(10):
        divs.append(Division(identifier=str(identifier + 4), style=style))

    return divs


def test_fill_area(ten_by_ten_div: Division):
    """Test that a component is filled correctly"""
    new_area = Compositor.fill_area(ten_by_ten_div, symbol="+")
    assert str(new_area) == """\
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++\
"""


def test_compose_one_child(
        ten_by_three_divs: list[Division],
        ten_by_ten_div: Division
):
    """Test that one child is composed correctly without column/row expansion
    """
    ten_by_ten_div._Component__area = Compositor.fill_area(
            ten_by_ten_div,
            symbol="+"
        )
    ten_by_three_divs[0]._Component__area = Compositor.fill_area(
            ten_by_three_divs[0],
            symbol="*"
        )
    ten_by_ten_div.append_child(ten_by_three_divs[0])

    assert str(Compositor.compose(ten_by_ten_div)) == """\
**********
**********
**********
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++\
"""


def test_compose_two_child(
        ten_by_three_divs: list[Division],
        ten_by_ten_div: Division
):
    """Test that two children are composed correctly"""
    ten_by_ten_div._area = Compositor.fill_area(
            ten_by_ten_div,
            symbol="+"
        )
    ten_by_three_divs[0]._area = Compositor.fill_area(
            ten_by_three_divs[0],
            symbol="*"
        )

    ten_by_three_divs[1]._area = Compositor.fill_area(
            ten_by_three_divs[1],
            symbol="#"
        )

    ten_by_ten_div.append_child(ten_by_three_divs[0])
    ten_by_ten_div.append_child(ten_by_three_divs[1])

    assert str(Compositor.compose(ten_by_ten_div)) == """\
**********
**********
**********
##########
##########
##########
++++++++++
++++++++++
++++++++++
++++++++++\
"""


def test_compose_child_that_exceeds_area_size(
        ten_by_three_divs: list[Division],
        ten_by_ten_div: Division
):
    """Test that an exception is thrown when there isn't enough area to compose
    the children of a component"""
    for i in range(4):
        ten_by_ten_div.append_child(ten_by_three_divs[i])

    with pytest.raises(InsufficientAreaError):
        Compositor.compose(ten_by_ten_div)


def test_compose_one_child_which_has_one_child(
        ten_by_ten_div: Division,
        ten_by_three_divs: list[Division],
        ten_by_one_divs: list[Division]
        ):
    """Test that a component with a child, which has a child, is composed
    correctly"""

    ten_by_ten_div.append_child(ten_by_three_divs[0])
    ten_by_ten_div._area = Compositor.fill_area(
            ten_by_ten_div,
            symbol=str("+")
        )

    ten_by_three_divs[0].append_child(ten_by_one_divs[0])

    ten_by_three_divs[0]._area = Compositor.fill_area(
            ten_by_three_divs[0],
            symbol=str("*")
        )

    ten_by_one_divs[0]._area = Compositor.fill_area(
            ten_by_one_divs[0],
            symbol=str("#")
        )

    assert str(Compositor.compose(ten_by_ten_div)) == """\
##########
**********
**********
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++
++++++++++\
"""


def test_compose_children_which_have_children(
        ten_by_ten_div: Division,
        ten_by_three_divs: list[Division],
        ten_by_one_divs: list[Division]
):
    """Test that a component with 3 children, which each have 3 children, is
    composed correctly"""

    ten_by_ten_div._area = Compositor.fill_area(
            ten_by_ten_div,
            symbol=str("+")
        )

    nested_children = 0  # second layer children counter
    for i in range(3):
        ten_by_ten_div.append_child(ten_by_three_divs[i])
        for _ in range(3):
            ten_by_three_divs[i].append_child(ten_by_one_divs[nested_children])

            ten_by_one_divs[nested_children]._area = Compositor.fill_area(
                    ten_by_one_divs[nested_children],
                    symbol=str(nested_children)
                )

            nested_children += 1

    ten_by_three_divs[0]._area = Compositor.fill_area(
            ten_by_three_divs[0],
            symbol=str("*")
        )

    ten_by_three_divs[1]._area = Compositor.fill_area(
            ten_by_three_divs[1],
            symbol=str("#")
        )

    ten_by_three_divs[2]._area = Compositor.fill_area(
            ten_by_three_divs[2],
            symbol=str("@")
        )

    assert str(Compositor.compose(ten_by_ten_div)) == """\
0000000000
1111111111
2222222222
3333333333
4444444444
5555555555
6666666666
7777777777
8888888888
++++++++++\
"""


def test_border(ten_by_ten_div):
    """Test that border is correctly applied to a component with no children"""
    new_area = Compositor.draw_border(ten_by_ten_div, symbol="+")
    assert str(new_area) == """\
++++++++++
+        +
+        +
+        +
+        +
+        +
+        +
+        +
+        +
++++++++++\
"""
