"""Describe how component composition should work"""

from dataclasses import dataclass
from enum import Enum, auto


class Orientation(Enum):
    """Hold orientation options for a component"""
    INLINE = auto()  # horizontal
    BLOCK = auto()  # vertical


@dataclass
class CompositorInfo:
    """Define properties that affect component composition"""
    # if the component's direct child has focus this component will also have
    # focus. Parent-most component steals focus from all it's children
    steal_focus: bool = False

    _display: Orientation = Orientation.BLOCK

    @property
    def display(self) -> Orientation:
        """Get a component's orientation"""
        return self._display

    @display.setter
    def display(self, display: str | Orientation) -> None:
        """Set component's orientation"""
        if isinstance(display, Orientation):
            self._display = display
            return

        self._display = Orientation[display.upper()]
