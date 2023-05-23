"""The input is a widget for capturing user input. It works as a dynamic label
as to where every new char the user writes forces a text update. Text can be
deleted with backspace."""

from typing import Optional

from tui.components.label import Label
from tui.events.event_broker import EventBroker
from tui.events.key_event import HotkeyEvent
from tui.events.keys import ANSI_SEQUENCES_KEYS, Keys
from tui.style import Style


class Input(Label):
    """A widget which once focused, stores the text a user enters."""
    def __init__(
            self,
            placeholder: str = "",
            style: str | Style = Style(),
            identifier: Optional[str] = None
    ) -> None:
        super().__init__(identifier=identifier,
                         style=style,
                         label_text=placeholder)

        self.placeholder = placeholder
        self.pos_pointer = 0

        def add_text_event(event: HotkeyEvent) -> None:
            """Handle how the input widget reacts when receiving keyboard
            events."""
            # Some events have multiple normal keys pressed at the same time
            # Make sure this isn't one of them
            if len(event.keys) != 1:
                return

            # Retrieve the only element in the set
            key = next(iter(event.keys))

            # If the key is backspace, try to remove one char
            if (key in ANSI_SEQUENCES_KEYS
                    and ANSI_SEQUENCES_KEYS[key][0] == "backspace"):
                self.remove_last_char()
                return

            # Key has to be a character
            if len(key) != 1:
                return

            self.add_text(key)

        EventBroker.subscribe(
                event=HotkeyEvent(Keys.Any),
                subscriber=self,
                pre_composition=add_text_event
        )

    def add_text(self, text: str) -> None:
        try:
            self.text = self.text[:self.pos_pointer] + text + "\x1b[30;47h  "
        except ValueError:  # not enough space
            return
        self.text = self.text[:-2]
        self.pos_pointer += len(text)

    def remove_last_char(self) -> None:
        # do nothing if text is empty
        if self.text.startswith("\x1b[30;47h") or len(self.text) < 1:
            return

        self.pos_pointer -= 1
        self.text = self.text[:self.pos_pointer] + "\x1b[30;47h  "
        self.text = self.text[:-2]

    def get_input(self) -> str:
        """Get the label's text"""
        return self._text.split("\x1b[30;47h")[0]
