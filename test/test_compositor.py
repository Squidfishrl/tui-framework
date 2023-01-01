import pytest

from tui.compositor import Compositor
from tui.components.division import Division
from tui.style import Style, AreaInfo


@pytest.fixture
def ten_by_ten_div():
    style = Style(area_info=AreaInfo(min_columns=10, min_rows=10))
    return Division(identifier="div1", style=style)


@pytest.fixture
def ten_by_three_div():
    style = Style(area_info=AreaInfo(min_columns=10, min_rows=3))
    return Division(identifier="child1", style=style)


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
    
        ten_by_three_div: Division,
        ten_by_ten_div: Division
    ):
    """Test that one child is composed correctly without column/row expansion
    """
    ten_by_ten_div._Component__area = Compositor.fill_area(ten_by_ten_div, symbol="+")
    ten_by_three_div._Component__area = Compositor.fill_area(ten_by_three_div, symbol="*")
    ten_by_ten_div.append_child(ten_by_three_div)

    print(str(Compositor.compose(ten_by_ten_div)))
    assert (str(Compositor.compose(ten_by_ten_div)) == """\
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
""")


def test_border(ten_by_ten_div):
    """Test that border is correctly applied to a component with no children"""
    new_area = Compositor.draw_border(ten_by_ten_div, symbol="+")
    assert (str(new_area) == """\
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
""")
