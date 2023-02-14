"""Describe how a widget's text should look"""

from dataclasses import dataclass
from enum import Enum, auto
import colorama as Colour


class TextAlignment(Enum):
    """Enum holding horizontal text alignment options"""
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class VerticalAlignment(Enum):
    """Enum holding vertical text alignment options"""
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()


@dataclass
class TextInfo:
    """Define properties for component colouring"""
    text_colour: str = Colour.Fore.WHITE
    text_background: str = Colour.Back.BLACK
    text_wrap: bool = True

    # tell Style that there's a _text_align property
    _text_align: TextAlignment = TextAlignment.LEFT

    # tell Style that there's a _vertical_align property
    _vertical_align: VerticalAlignment = VerticalAlignment.TOP

    @property
    def text_align(self) -> TextAlignment:
        """Get text's alignment setting"""
        return self._text_align

    @text_align.setter
    def text_align(self, text_align: str | TextAlignment) -> None:
        """Set the text's alignment"""
        if isinstance(text_align, TextAlignment):
            self._text_align = text_align
            return

        self._text_align = TextAlignment[text_align.upper()]

    @property
    def vertical_align(self) -> VerticalAlignment:
        """Get the text's vertical alignment"""
        return self._vertical_align

    @vertical_align.setter
    def vertical_align(self, vertical_align: str | VerticalAlignment) -> None:
        """Set the text's vertical alignment"""
        if isinstance(vertical_align, VerticalAlignment):
            self._vertical_align = vertical_align
            return

        self._vertical_align = VerticalAlignment[vertical_align.upper()]
