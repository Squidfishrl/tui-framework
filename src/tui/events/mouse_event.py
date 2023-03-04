"""The Mouse Event reports most 3 button mouse actions. Do note that some
terminals cannot report mouse events. Double and Triple click events aren't
reported or software implemented."""

from tui._coordinates import Coordinates
from tui.events.event import Event
from tui.events.mouse import MouseAction, MouseButton, MouseEventTypes


class MouseEvent(Event):
    """The MouseEvent is reported on any mouse action. It's responsible for
    defining the event type and reporting the cursor's coordinates it occurred
    on."""
    def __init__(
            self,
            coordinates: Coordinates,
            event_type: MouseEventTypes
    ) -> None:
        self.__coordinates = coordinates
        self.__event = event_type
        super().__init__(self.event.value.modifiers)

    @property
    def action(self) -> MouseAction:
        """Get mouse action."""
        return self.__event.value.action

    @property
    def button(self) -> MouseButton:
        """Get mouse button."""
        return self.__event.value.button

    @property
    def event(self) -> MouseEventTypes:
        """Get mouse event type."""
        return self.__event

    @property
    def coordinates(self) -> Coordinates:
        """Get mouse cursor coordinates."""
        return self.__coordinates

    def __repr__(self) -> str:
        return f"({self.coordinates} - {self.event})"
