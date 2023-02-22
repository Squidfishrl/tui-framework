from __future__ import annotations

from enum import Enum
from typing import FrozenSet, Mapping
from tui._coordinates import Coordinates


class MouseEvent:
    """Class holding all information regarding a mouse event."""
    def __init__(
            self,
            coordinates: Coordinates,
            action: MouseAction,
            button: MouseButton,
            modifiers: FrozenSet[MouseModifier]
    ) -> None:
        self.coordinates = coordinates
        self.action = action
        self.button = button
        self.modifiers = modifiers

    def __repr__(self) -> str:
        return f"\
{self.coordinates}, {self.action}, {self.button}, {self.modifiers}\
"


class MouseAction(Enum):
    """Enum holding the possible mouse events."""

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
    """Enum holding the possible mouse button states."""
    LEFT = "LEFT"
    MIDDLE = "MIDDLE"
    RIGHT = "RIGHT"
    NONE = "NONE"  # On mouse move or scroll


class MouseModifier(Enum):
    """Enum holding the possible mouse modifiers."""
    SHIFT = "SHIFT"
    ALT = "ALT"
    CONTROL = "CONTROL"


# Mouse control sequence translated for most xterms
xterm_code_map: Mapping[str, tuple[MouseAction, MouseButton, list[MouseModifier]]] = {
    "35": (MouseAction.MOUSE_MOVE, MouseButton.NONE, []),
    "39": (MouseAction.MOUSE_MOVE, MouseButton.NONE, [MouseModifier.SHIFT]),
    "43": (MouseAction.MOUSE_MOVE, MouseButton.NONE, [MouseModifier.ALT]),
    "47": (MouseAction.MOUSE_MOVE, MouseButton.NONE, [MouseModifier.ALT, MouseModifier.SHIFT]),
    "51": (MouseAction.MOUSE_MOVE, MouseButton.NONE, [MouseModifier.CONTROL]),
    "55": (MouseAction.MOUSE_MOVE, MouseButton.NONE, [MouseModifier.CONTROL, MouseModifier.SHIFT]),
    "0": (MouseAction.MOUSE_UP, MouseButton.LEFT, []),
    "8": (MouseAction.MOUSE_UP, MouseButton.LEFT, [MouseModifier.ALT]),
    "16": (MouseAction.MOUSE_UP, MouseButton.LEFT, [MouseModifier.CONTROL]),
    "32": (MouseAction.MOUSE_DRAG, MouseButton.LEFT, []),
    "1": (MouseAction.MOUSE_UP, MouseButton.MIDDLE, []),
    "9": (MouseAction.MOUSE_UP, MouseButton.MIDDLE, [MouseModifier.ALT]),
    "17": (MouseAction.MOUSE_UP, MouseButton.MIDDLE, [MouseModifier.CONTROL]),
    "33": (MouseAction.MOUSE_DRAG, MouseButton.MIDDLE, []),
    "2": (MouseAction.MOUSE_UP, MouseButton.RIGHT, []),
    "10": (MouseAction.MOUSE_UP, MouseButton.RIGHT, [MouseModifier.ALT]),
    "18": (MouseAction.MOUSE_UP, MouseButton.RIGHT, [MouseModifier.CONTROL]),
    "34": (MouseAction.MOUSE_DRAG, MouseButton.RIGHT, []),
    "64": (MouseAction.SCROLL_UP, MouseButton.NONE, []),
    "68": (MouseAction.SCROLL_UP, MouseButton.NONE, [MouseModifier.SHIFT]),
    "72": (MouseAction.SCROLL_UP, MouseButton.NONE, [MouseModifier.ALT]),
    "76": (MouseAction.SCROLL_UP, MouseButton.NONE, [MouseModifier.ALT, MouseModifier.SHIFT]),
    "80": (MouseAction.SCROLL_UP, MouseButton.NONE, [MouseModifier.CONTROL]),
    "84": (MouseAction.SCROLL_UP, MouseButton.NONE, [MouseModifier.CONTROL, MouseModifier.SHIFT]),
    "65": (MouseAction.SCROLL_DOWN, MouseButton.NONE, []),
    "69": (MouseAction.SCROLL_DOWN, MouseButton.NONE, [MouseModifier.SHIFT]),
    "73": (MouseAction.SCROLL_DOWN, MouseButton.NONE, [MouseModifier.ALT]),
    "77": (MouseAction.SCROLL_DOWN, MouseButton.NONE, [MouseModifier.ALT, MouseModifier.SHIFT]),
    "81": (MouseAction.SCROLL_DOWN, MouseButton.NONE, [MouseModifier.CONTROL]),
    "85": (MouseAction.SCROLL_DOWN, MouseButton.NONE, [MouseModifier.CONTROL, MouseModifier.SHIFT]),
}
