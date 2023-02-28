
from functools import cache
import re

from tui._coordinates import Coordinates
from tui.events.mouse import MouseEventTypes, xterm_code_map
from tui.events.mouse_event import MouseEvent


class MouseParser:
    """Class for parsing VT100 mouse events"""
    # capture mouse event info
    mouse_event_capture: re.Pattern

    @staticmethod
    @cache
    def get_mouse_event(control_code: str) -> MouseEvent:
        """Convert a VT100 mouse control code to a MouseEvent object."""
        try:
            _type, column, row, release = re.findall(
                    MouseParser.mouse_event_capture,
                    control_code
                )[0]
        except IndexError:
            # Mouse coordinates are out of bounds
            return MouseEvent(
                coordinates=Coordinates(_row=-1, _column=-1),
                event_type=MouseEventTypes.MOUSE_UNKNOWN
            )

        # TODO: handle MOUSE_DOWN
        release = True if release == 'm' else False

        event_type = xterm_code_map.get(_type)
        coords = Coordinates(_row=int(row), _column=int(column))
        if event_type is None:
            return MouseEvent(
                coordinates=coords,
                event_type=MouseEventTypes.MOUSE_UNKNOWN
            )

        return MouseEvent(
                coordinates=coords,
                event_type=event_type
        )


# \x1b[<0;99;20M
MouseParser.mouse_event_capture = re.compile(r"""
(?: # control code
\x1b # CSI (escaping `\` isn't necessary)
\[<
(\d+) # event type
;
(\d+) # column
;
(\d+) # row
([m|M]) # hold or release
)
""", re.VERBOSE)
