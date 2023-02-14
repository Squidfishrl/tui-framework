"""Test that src/components/label.py works correctly"""

import pytest

from tui.components.label import Label


def test_label_init():
    """Test that a label is initialized correctly"""
    lbl = Label(style="rows=1,columns=10", label_text="Hello!")
    assert str(lbl.area) == """Hello!    """


def test_label_invalid_init():
    """Test that a label throws an exception when text can't fit"""
    with pytest.raises(ValueError):
        _ = Label(style="rows=1,columns=10", label_text="Hello, World!")


def test_label_center_text():
    """Test that a one-line text in centered"""
    lbl = Label(style="rows=1, columns=10, text_align=center", label_text="hi")
    assert str(lbl.area) == "    hi    "


def test_label_right_aligned_text():
    """Test that a one-line text in aligned to the right"""
    lbl = Label(style="rows=1, columns=10, text_align=right", label_text="hi")
    assert str(lbl.area) == "        hi"


def test_label_multiline_centered_text():
    """Test that a multi-line centered text is centered"""
    lbl = Label(
        style="rows=5, columns=10, text_align=center",
        label_text="Hello\nWorld\nLine 3"
    )

    print(lbl.area)
    assert str(lbl.area) == """\
  Hello   
  World   
  Line 3  
          
          \
"""


def test_label_vertical_center_text():
    """Test that a one-line text is centered vertically"""
    lbl = Label(
            style="rows=3, columns=5, vertical_align=center",
            label_text="hi"
        )
    assert str(lbl.area) == """\
     
hi   
     \
"""


def test_label_vertical_bottom_text():
    """Test that a one-line text in vertically at the bottom of its area"""
    lbl = Label(
            style="rows=3, columns=5, vertical_align=bottom",
            label_text="hi"
        )
    assert str(lbl.area) == """\
     
     
hi   \
"""


def test_label_vertical_center_multiline_text():
    """Test that multi-line text is centered vertically"""
    lbl = Label(
            style="rows=8, columns=5, vertical_align=center",
            label_text="Hello\nWorld\nTest"
        )
    assert str(lbl.area) == """\
     
     
Hello
World
Test 
     
     
     \
"""


def test_label_absolute_center_multiline_text():
    """Test that multi-line text is centered vertically and horizontally"""
    lbl = Label(
            style="rows=8, columns=10, vertical_align=center,\
                    text_align=center",
            label_text="Hello\nWorld\nTest"
        )
    assert str(lbl.area) == """\
          
          
  Hello   
  World   
   Test   
          
          
          \
"""
