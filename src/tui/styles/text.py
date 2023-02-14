"""Describe how a widget's text should look"""

from dataclasses import dataclass
from enum import Enum, auto
import colorama as Colour


class TextAlignment(Enum):
    """Enum holding different text alignment options"""
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


@dataclass
class TextInfo:
    """Define properties for component colouring"""
    text_colour: str = Colour.Fore.WHITE
    text_background: str = Colour.Back.BLACK

    # tell style that there's a _text_align property
    _text_align: TextAlignment = TextAlignment.CENTER

    @property
    def text_align(self) -> TextAlignment:
        return self._text_align

    @text_align.setter
    def text_align(self, text_align: str | TextAlignment) -> None:
        if isinstance(text_align, TextAlignment):
            self._text_align = text_align
            return

        self._text_align = TextAlignment[text_align]
