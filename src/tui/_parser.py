"""All regex patterns can be found here. This is done, as to not pollute the
other classes with long regex patterns."""

from functools import cache
import re

from tui._coordinates import Coordinates
from tui.mouse import MouseAction, MouseButton, MouseEvent, xterm_code_map


class Parser:
    """Responsible for holding all regex patters"""

    # validate that string format is correct and can be converted to a style
    valid_str_to_style_pattern: re.Pattern
    # used for fetching attribute-value pairs from a style string
    style_str_to_attr_and_val: re.Pattern

    # capture mouse event info
    mouse_event_capture: re.Pattern

    @staticmethod
    @cache
    def get_mouse_event(control_code: str) -> MouseEvent:
        """Convert a VT100 mouse control code to a MouseEvent object."""
        _type, column, row, release = re.findall(
                Parser.mouse_event_capture,
                control_code
            )[0]

        event_info = xterm_code_map.get(_type)
        if event_info is not None:
            action = MouseAction.MOUSE_DOWN if release == 'm' else event_info[0]
            btn = event_info[1]
            modifiers = frozenset(event_info[2])
        else:
            action = MouseAction.UNKNOWN
            btn = MouseButton.NONE
            modifiers = frozenset()

        return MouseEvent(
                coordinates=Coordinates(_row=int(row), _column=int(column)),
                action=action,
                button=btn,
                modifiers=modifiers
            )

    @staticmethod
    @cache
    def auto_wrap_text(max_width: int):
        """Used to split text into smaller parts"""
        return re.compile("(.{0," + str(max_width) + "})(?: | ?$)")


Parser.valid_str_to_style_pattern = re.compile(r"""
[ \n]* # non strict newlines and whitespaces
(?:\w+) # attribute name
[ \n]*
=
[ \n]*
(?:\w+|\d+) # attribute value (string or whole number)
(?: # group for multiple attribute-value pairs
[ \n]*
, # separator for attribute-value pairs
[ \n]*
(?:\w+)
[ \n]*
=
[ \n]*
(?:\w+|\d+)
)* # can have any amount of attribute-value pairs
[ \n]*
,? # can end with or without a comma
[ \n]*
""", re.VERBOSE)

Parser.style_str_to_attr_and_val = re.compile(r"""
(?: # group attribute-value pairs
(\w+) # get attribute name
[ \n]* # non strict newlines and whitespaces
=
[ \n]*
(\w+|\d+) # get attribute value (string or integer)
)* # repeat group for every pair
""", re.VERBOSE)

# \x1b[<0;99;20M
Parser.mouse_event_capture = re.compile(r"""
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
