import pytest

from tui.compositor import Compositor, InsufficientAreaError
from tui.components.division import Division
from tui.style import Style, AreaInfo


@pytest.fixture
def ten_by_ten_div():
    style = Style(area_info=AreaInfo(min_columns=10, min_rows=10))
    style.compositor_info.inline=True
    return Division(identifier="div1", style=style)


@pytest.fixture
def three_by_ten_divs():
    style = Style(area_info=AreaInfo(min_columns=3, min_rows=10))
    style.compositor_info.inline=True
    divs = []

    for id in range(20):
        divs.append(Division(identifier=str(id), style=style))

    return divs


@pytest.fixture
def one_by_ten_divs():
    style = Style(area_info=AreaInfo(min_columns=1, min_rows=10))
    divs = []

    for id in range(60):
        divs.append(Division(identifier=str(id + 20), style=style))

    return divs


def test_fill_area(ten_by_ten_div: Division):
    """Test that a component is filled correctly"""
    new_area = Compositor.fill_area(ten_by_ten_div, symbol="+")
    assert (str(new_area) == """\
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
""")


def test_compose_one_child(
        three_by_ten_divs: list[Division],
        ten_by_ten_div: Division
    ):
    """Test that one child is composed correctly without column/row expansion
    """
    ten_by_ten_div._Component__area = Compositor.fill_area(
            ten_by_ten_div,
            symbol="+"
        )
    three_by_ten_divs[0]._Component__area = Compositor.fill_area(
            three_by_ten_divs[0],
            symbol="*"
        )
    ten_by_ten_div.append_child(three_by_ten_divs[0])

    assert (str(Compositor.compose(ten_by_ten_div)) == """\
***+++++++
***+++++++
***+++++++
***+++++++
***+++++++
***+++++++
***+++++++
***+++++++
***+++++++
***+++++++\
""")


def test_compose_two_child(
        three_by_ten_divs: list[Division],
        ten_by_ten_div: Division
    ):
    """Test that two children are composed correctly"""
    ten_by_ten_div._area = Compositor.fill_area(
            ten_by_ten_div,
            symbol="+"
        )
    three_by_ten_divs[0]._area = Compositor.fill_area(
            three_by_ten_divs[0],
            symbol="*"
        )

    three_by_ten_divs[1]._area = Compositor.fill_area(
            three_by_ten_divs[1],
            symbol="#"
        )

    ten_by_ten_div.append_child(three_by_ten_divs[0])
    ten_by_ten_div.append_child(three_by_ten_divs[1])

    assert (str(Compositor.compose(ten_by_ten_div)) == """\
***###++++
***###++++
***###++++
***###++++
***###++++
***###++++
***###++++
***###++++
***###++++
***###++++\
""")


def test_compose_child_that_exceeds_area_size(
        three_by_ten_divs: list[Division],
        ten_by_ten_div: Division
    ):
    """Test that an exception is thrown when there isn't enough area to compose
    the children of a component"""
    for i in range(4):
        ten_by_ten_div.append_child(three_by_ten_divs[i])

    with pytest.raises(InsufficientAreaError):
        Compositor.compose(ten_by_ten_div)


def test_compose_one_child_which_has_one_child(
        ten_by_ten_div: Division,
        three_by_ten_divs: list[Division],
        one_by_ten_divs: list[Division]
        ):
    """Test that a component with a child, which has a child, is composed
    correctly"""

    ten_by_ten_div.append_child(three_by_ten_divs[0])
    ten_by_ten_div._area = Compositor.fill_area(
            ten_by_ten_div,
            symbol=str("+")
        )

    three_by_ten_divs[0].append_child(one_by_ten_divs[0])

    three_by_ten_divs[0]._area = Compositor.fill_area(
            three_by_ten_divs[0],
            symbol=str("*")
        )

    one_by_ten_divs[0]._area = Compositor.fill_area(
            one_by_ten_divs[0],
            symbol=str("#")
        )

    assert (str(Compositor.compose(ten_by_ten_div)) == """\
#**+++++++
#**+++++++
#**+++++++
#**+++++++
#**+++++++
#**+++++++
#**+++++++
#**+++++++
#**+++++++
#**+++++++\
""")

def test_compose_children_which_have_children(
        ten_by_ten_div: Division,
        three_by_ten_divs: list[Division],
        one_by_ten_divs: list[Division]
        ):
    """Test that a component with 3 children, which each have 3 children, is 
    composed correctly"""

    ten_by_ten_div._area = Compositor.fill_area(
            ten_by_ten_div,
            symbol=str("+")
        )

    nested_children = 0 # second layer children counter
    for i in range(3):
        ten_by_ten_div.append_child(three_by_ten_divs[i])
        for _ in range(3):
            three_by_ten_divs[i].append_child(one_by_ten_divs[nested_children])

            one_by_ten_divs[nested_children]._area = Compositor.fill_area(
                    one_by_ten_divs[nested_children],
                    symbol=str(nested_children)
                )

            nested_children += 1

    three_by_ten_divs[0]._area = Compositor.fill_area(
            three_by_ten_divs[0],
            symbol=str("*")
        )

    three_by_ten_divs[1]._area = Compositor.fill_area(
            three_by_ten_divs[1],
            symbol=str("#")
        )

    three_by_ten_divs[2]._area = Compositor.fill_area(
            three_by_ten_divs[2],
            symbol=str("@")
        )

    assert (str(Compositor.compose(ten_by_ten_div)) == """\
012345678+
012345678+
012345678+
012345678+
012345678+
012345678+
012345678+
012345678+
012345678+
012345678+\
""")
