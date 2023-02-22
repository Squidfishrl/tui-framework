"""App handles other modules and prints the application to the terminal"""

from __future__ import annotations

import time
import threading
from typing import Optional, TYPE_CHECKING
from queue import Queue

import colorama

from tui._coordinates import Coordinates
from tui.components.container import Container
from tui.compositor import Compositor
from tui.event_broker import EventBroker
from tui.mouse import MouseAction, MouseButton, MouseEvent
from tui.styles.border import DefaultBorder
from tui.terminal import Terminal
from tui.components.division import Division

if TYPE_CHECKING:
    from tui.keys import Keys


class App():
    """Contains everything necessary for running the application."""
    def __init__(
            self,
            fps: int = 60,  # frames per second
            # static row and col amount (in case terminal fails)
            rows: Optional[int] = None,
            columns: Optional[int] = None,
    ) -> None:
        # Instance of the terminal the app is being ran in
        try:
            self.__terminal: Terminal = Terminal()
            rows = self.__terminal.rows
            columns = self.__terminal.columns
        except OSError:
            pass

        self.event_queue: Queue[str | tuple[Keys] | MouseEvent] = Queue()
        self.frequency = 1 / fps

        # Create a root element with the size of the terminal resolution
        self._root = Division(style=f"rows={rows}, columns={columns}")
        self.root = self._root

    @property
    def root(self) -> Container:
        """Get the root component"""
        return self._root

    @root.setter
    def root(self, new_root: Container) -> None:
        """Change the root component"""
        EventBroker.unsubscribe_all(self.root)
        self._root = new_root

        def draw_cursor(event: str | tuple[Keys] | MouseEvent):
            area = self._root.area.char_area
            area[event.coordinates.row][event.coordinates.column] = colorama.Fore.BLACK + colorama.Back.WHITE + area[event.coordinates.row][event.coordinates.column] + colorama.Style.RESET_ALL

        EventBroker.subscribe(
                MouseEvent(
                    coordinates=Coordinates(0, 0),
                    action=MouseAction.MOUSE_MOVE,
                    button=MouseButton.NONE,
                    modifiers=frozenset()
                ),
                subscriber=self._root,
                post_composition=lambda event: draw_cursor(event),
                local=False
            )

    def get_events(self) -> None:
        """Continuously fetch events and put them in the event queue."""
        from tui._parser import Parser
        from tui.keys import ANSI_SEQUENCES_KEYS

        while True:
            # read from stdin
            control_code = self.__terminal.read_bytes(bytes=16).decode()
            # check if it's a control sequence or a simple key press
            if len(control_code) == 1:
                self.event_queue.put(control_code)
                continue

            # check if it's a mouse control code and add to the event queue
            # TODO: verify without raising exceptions
            try:
                self.event_queue.put(ANSI_SEQUENCES_KEYS[control_code])
            except KeyError:
                self.event_queue.put(Parser.get_mouse_event(control_code))

    def run(self) -> None:
        """Start and constantly update the app."""
        input_thread = threading.Thread(
                target=self.get_events,
                args=(),
                daemon=True
            )

        input_thread.start()

        try:
            while True:
                if self.event_queue.qsize() > 0:
                    event = self.event_queue.get()
                    pre_composit_hooks, post_composit_hooks = EventBroker.handle(event)
                    print(Compositor.compose(
                                            self.root,
                                            pre_composit=pre_composit_hooks,
                                            post_composit=post_composit_hooks,
                                            event=event),
                          end='')

                time.sleep(self.frequency)
        except KeyboardInterrupt:
            self.__terminal.disable_mouse()
            self.__terminal.disable_input()
        except BaseException as e:
            self.__terminal.disable_mouse()
            self.__terminal.disable_input()
            raise e


def main():
    """Run an app"""
    app: App = App()
    app.root.add_border(DefaultBorder)
    app.run()


if __name__ == "__main__":
    main()
