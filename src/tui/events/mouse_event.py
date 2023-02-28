"""Mouse events"""

from typing import FrozenSet
from tui._coordinates import Coordinates
from tui.events.event import Event, Modifiers
from tui.events.mouse import MouseAction, MouseButton, MouseEventTypes


class MouseEvent(Event):
    """Class holding all information regarding a mouse event."""
    def __init__(
            self,
            coordinates: Coordinates,
            event_type: MouseEventTypes
    ) -> None:
        self.__coordinates = coordinates
        self.__event = event_type

    @property
    def modifiers(self) -> FrozenSet[Modifiers]:
        """Get modifiers"""
        return self.__event.value.modifiers

    @property
    def action(self) -> MouseAction:
        """Get mouse action"""
        return self.__event.value.action

    @property
    def button(self) -> MouseButton:
        """Get mouse button"""
        return self.__event.value.button

    @property
    def event(self) -> MouseEventTypes:
        """Get mouse event type"""
        return self.__event

    @property
    def coordinates(self) -> Coordinates:
        """Get mouse cursor coordinates"""
        return self.__coordinates

    def __repr__(self) -> str:
        return f"({self.coordinates} - {self.event})"
