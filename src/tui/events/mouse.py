"""Defines possible mouse events and maps them to their corresponding codes.
A mouse event can be segregated into a mouse action, button click and key
modifiers."""

from __future__ import annotations

from enum import Enum
from typing import Mapping
from tui.events.event import Event, Modifiers


class MouseAction(Enum):
    """Enum responsible or holding all possible mouse events."""

    # Triggered when mouse changes coordinates.
    MOUSE_MOVE = "MOUSE_MOVE"
    # Triggered on mouse click
    MOUSE_UP = "MOUSE_UP"
    # Triggered on mouse click release
    MOUSE_DOWN = "MOUSE_DOWN"
    # Triggered on mouse drag (MOUSE_UP and MOUSE_MOVE at the same time)
    MOUSE_DRAG = "MOUSE_DRAG"

    SCROLL_UP = "SCROLL_UP"
    SCROLL_DOWN = "SCROLL_DOWN"

    UNKNOWN = "UNKNOWN"


class MouseButton(Enum):
    """Enum responsible for holding the possible mouse button states."""
    LEFT = "LEFT"
    MIDDLE = "MIDDLE"
    RIGHT = "RIGHT"
    NONE = "NONE"  # On mouse move or scroll


class _MouseEvent(Event):
    """Mouse event without the coordinates. Event listeners are subscribed to
    this event type since coordinates aren't required for the event"""
    def __init__(
            self,
            action: MouseAction,
            button: MouseButton,
            modifiers: list[str]
    ) -> None:
        self.action = action
        self.button = button
        # convert modifier str to Modifier enum
        self.modifiers = frozenset(map(lambda x: Modifiers(x), modifiers))


class MouseEventTypes(Enum):
    """Enum responsible for holding the possible mouse events and their class
    instances."""
    MOUSE_MOVE = _MouseEvent(action=MouseAction.MOUSE_MOVE,
                             button=MouseButton.NONE,
                             modifiers=[])

    MOUSE_SHIFT_MOVE = _MouseEvent(action=MouseAction.MOUSE_MOVE,
                                   button=MouseButton.NONE,
                                   modifiers=[Modifiers.SHIFT])

    MOUSE_ALT_MOVE = _MouseEvent(action=MouseAction.MOUSE_MOVE,
                                 button=MouseButton.NONE,
                                 modifiers=[Modifiers.ALT])

    MOUSE_ALT_SHIFT_MOVE = _MouseEvent(action=MouseAction.MOUSE_MOVE,
                                       button=MouseButton.NONE,
                                       modifiers=[Modifiers.ALT,
                                                  Modifiers.SHIFT])
    MOUSE_CONTROL_MOVE = _MouseEvent(action=MouseAction.MOUSE_MOVE,
                                     button=MouseButton.NONE,
                                     modifiers=[Modifiers.CONTROL])
    MOUSE_CONTROL_SHIFT_MOVE = _MouseEvent(action=MouseAction.MOUSE_MOVE,
                                           button=MouseButton.NONE,
                                           modifiers=[Modifiers.CONTROL,
                                                      Modifiers.SHIFT])
    MOUSE_LEFT_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                   button=MouseButton.LEFT,
                                   modifiers=[])
    MOUSE_ALT_LEFT_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                       button=MouseButton.LEFT,
                                       modifiers=[Modifiers.ALT])
    MOUSE_CONTROL_LEFT_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                           button=MouseButton.LEFT,
                                           modifiers=[Modifiers.CONTROL])
    MOUSE_LEFT_CLICK_DRAG = _MouseEvent(action=MouseAction.MOUSE_DRAG,
                                        button=MouseButton.LEFT,
                                        modifiers=[])
    MOUSE_MIDDLE_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                     button=MouseButton.MIDDLE,
                                     modifiers=[])
    MOUSE_ALT_MIDDLE_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                         button=MouseButton.MIDDLE,
                                         modifiers=[Modifiers.ALT])
    MOUSE_CONTROL_MIDDLE_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                             button=MouseButton.MIDDLE,
                                             modifiers=[Modifiers.CONTROL])
    MOUSE_MIDDLE_CLICK_DRAG = _MouseEvent(action=MouseAction.MOUSE_DRAG,
                                          button=MouseButton.MIDDLE,
                                          modifiers=[])
    MOUSE_RIGHT_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                    button=MouseButton.RIGHT,
                                    modifiers=[])
    MOUSE_ALT_RIGHT_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                        button=MouseButton.RIGHT,
                                        modifiers=[Modifiers.ALT])
    MOUSE_CONTROL_RIGHT_CLICK = _MouseEvent(action=MouseAction.MOUSE_UP,
                                            button=MouseButton.RIGHT,
                                            modifiers=[Modifiers.CONTROL])
    MOUSE_RIGHT_CLICK_DRAG = _MouseEvent(action=MouseAction.MOUSE_DRAG,
                                         button=MouseButton.RIGHT,
                                         modifiers=[])
    MOUSE_SCROLL_UP = _MouseEvent(action=MouseAction.SCROLL_UP,
                                  button=MouseButton.NONE,
                                  modifiers=[])
    MOUSE_SHIFT_SCROLL_UP = _MouseEvent(action=MouseAction.SCROLL_UP,
                                        button=MouseButton.NONE,
                                        modifiers=[Modifiers.SHIFT])
    MOUSE_ALT_SCROLL_UP = _MouseEvent(action=MouseAction.SCROLL_UP,
                                      button=MouseButton.NONE,
                                      modifiers=[Modifiers.ALT])
    MOUSE_ALT_SHIFT_SCROLL_UP = _MouseEvent(action=MouseAction.SCROLL_UP,
                                            button=MouseButton.NONE,
                                            modifiers=[Modifiers.ALT,
                                                       Modifiers.SHIFT])
    MOUSE_CONTROL_SCROLL_UP = _MouseEvent(action=MouseAction.SCROLL_UP,
                                          button=MouseButton.NONE,
                                          modifiers=[Modifiers.CONTROL])
    MOUSE_CONTROL_SHIFT_SCROLL_UP = _MouseEvent(action=MouseAction.SCROLL_UP,
                                                button=MouseButton.NONE,
                                                modifiers=[Modifiers.CONTROL,
                                                           Modifiers.SHIFT])
    MOUSE_SCROLL_DOWN = _MouseEvent(action=MouseAction.SCROLL_DOWN,
                                    button=MouseButton.NONE,
                                    modifiers=[])
    MOUSE_SHIFT_SCROLL_DOWN = _MouseEvent(action=MouseAction.SCROLL_DOWN,
                                          button=MouseButton.NONE,
                                          modifiers=[Modifiers.SHIFT])
    MOUSE_ALT_SCROLL_DOWN = _MouseEvent(action=MouseAction.SCROLL_DOWN,
                                        button=MouseButton.NONE,
                                        modifiers=[Modifiers.ALT])
    MOUSE_ALT_SHIFT_SCROLL_DOWN = _MouseEvent(action=MouseAction.SCROLL_DOWN,
                                              button=MouseButton.NONE,
                                              modifiers=[Modifiers.ALT,
                                                         Modifiers.SHIFT])
    MOUSE_CONTROL_SCROLL_DOWN = _MouseEvent(action=MouseAction.SCROLL_DOWN,
                                            button=MouseButton.NONE,
                                            modifiers=[Modifiers.CONTROL])
    MOUSE_CONTROL_SHIFT_SCROLL_DOWN = _MouseEvent(
            action=MouseAction.SCROLL_DOWN,
            button=MouseButton.NONE,
            modifiers=[Modifiers.CONTROL,
                       Modifiers.SHIFT])
    # used for unknown codes
    MOUSE_UNKNOWN = _MouseEvent(action=MouseAction.UNKNOWN,
                                button=MouseButton.NONE,
                                modifiers=[])


# Mouse control sequences mapped for most xterms to the corresponding mouse
# event type
xterm_code_map: Mapping[str, MouseEventTypes] = {
    "35": MouseEventTypes.MOUSE_MOVE,
    "39": MouseEventTypes.MOUSE_SHIFT_MOVE,
    "43": MouseEventTypes.MOUSE_ALT_MOVE,
    "47": MouseEventTypes.MOUSE_ALT_SHIFT_MOVE,
    "51": MouseEventTypes.MOUSE_CONTROL_MOVE,
    "55": MouseEventTypes.MOUSE_CONTROL_SHIFT_MOVE,
    "0": MouseEventTypes.MOUSE_LEFT_CLICK,
    "8": MouseEventTypes.MOUSE_ALT_LEFT_CLICK,
    "16": MouseEventTypes.MOUSE_CONTROL_LEFT_CLICK,
    "32": MouseEventTypes.MOUSE_LEFT_CLICK_DRAG,
    "1": MouseEventTypes.MOUSE_MIDDLE_CLICK,
    "9": MouseEventTypes.MOUSE_ALT_MIDDLE_CLICK,
    "17": MouseEventTypes.MOUSE_CONTROL_MIDDLE_CLICK,
    "33": MouseEventTypes.MOUSE_MIDDLE_CLICK_DRAG,
    "2": MouseEventTypes.MOUSE_RIGHT_CLICK,
    "10": MouseEventTypes.MOUSE_ALT_RIGHT_CLICK,
    "18": MouseEventTypes.MOUSE_CONTROL_RIGHT_CLICK,
    "34": MouseEventTypes.MOUSE_RIGHT_CLICK_DRAG,
    "64": MouseEventTypes.MOUSE_SCROLL_UP,
    "68": MouseEventTypes.MOUSE_SHIFT_SCROLL_UP,
    "72": MouseEventTypes.MOUSE_ALT_SCROLL_UP,
    "76": MouseEventTypes.MOUSE_ALT_SHIFT_SCROLL_UP,
    "80": MouseEventTypes.MOUSE_CONTROL_SCROLL_UP,
    "84": MouseEventTypes.MOUSE_CONTROL_SHIFT_SCROLL_UP,
    "65": MouseEventTypes.MOUSE_SCROLL_DOWN,
    "69": MouseEventTypes.MOUSE_SHIFT_SCROLL_DOWN,
    "73": MouseEventTypes.MOUSE_ALT_SCROLL_DOWN,
    "77": MouseEventTypes.MOUSE_ALT_SHIFT_SCROLL_DOWN,
    "81": MouseEventTypes.MOUSE_CONTROL_SCROLL_DOWN,
    "85": MouseEventTypes.MOUSE_CONTROL_SHIFT_SCROLL_DOWN
}
