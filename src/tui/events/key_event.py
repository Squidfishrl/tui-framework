"""Key event"""

from tui.events.event import Event, Modifiers
from tui.events.keys import Keys


class HotkeyEvent(Event):
    """Key Event"""
    def __init__(
            self,
            hotkeys: str | tuple[str, ...] | Keys | tuple[Keys, ...]
    ) -> None:
        # convert hotkey to tuple for unified parsing
        if not isinstance(hotkeys, tuple):
            hotkeys = tuple(hotkeys)

        # keys such as escape are also stored here
        normal_keys: list[str] = []  # normal key press
        modifier_list = []

        for hotkey in hotkeys:
            # split keys on '+' (as is in src/tui/events/keys.py)
            keys = hotkey.split(sep='+')
            for key in keys:
                if Modifiers.contains(key):
                    modifier_list.append(Modifiers(key))
                else:
                    # there can be only one key which isn't a modifier
                    normal_keys.append(key)

        self.keys = frozenset(normal_keys)
        self.modifiers = frozenset(modifier_list)
