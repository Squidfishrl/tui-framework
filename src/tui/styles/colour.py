"""Describe how a component should be coloured"""

from dataclasses import dataclass
import colorama as Colour


@dataclass
class ColourInfo:
    """Define properties for component colouring"""
    foreground: Colour.Fore = Colour.Fore.WHITE
    background: Colour.Back = Colour.Back.BLACK
