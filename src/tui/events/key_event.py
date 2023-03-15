"""The Hotkey Event reports single key presses as well as a complex combination
of keys(hotkey). Do note that some terminals cannot report keys in VT100 mode,
or they might use a different bytes for reporting them which can result in
limited/false events being reported."""

from __future__ import annotations

from tui.events.event import Event, Modifiers
from tui.events.keys import Keys


class HotkeyEvent(Event):
    """The HotkeyEvent is triggered on a button press. It's responsible for
    describing the event - a key with what modifiers was pressed?"""
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
        super().__init__(frozenset(modifier_list))

    def __eq__(self, __o: HotkeyEvent) -> bool:
        return self.keys == __o.keys and self.modifiers == __o.modifiers

    def __hash__(self) -> int:
        return (str(self.keys.__hash__()) +
                str(self.modifiers.__hash__())).__hash__()
