"""App handles other modules and prints the application to the terminal"""

from __future__ import annotations

import threading
from typing import Optional
from queue import Queue

import colorama

from tui._coordinates import Coordinates
from tui.components.container import Container
from tui.compositor import Compositor
from tui.events.event import Event
from tui.events.event_broker import EventBroker
from tui.events.mouse import MouseEventTypes
from tui.events.mouse_event import MouseEvent
from tui.styles.border import DefaultBorder
from tui.terminal import Terminal
from tui.components.division import Division


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
        self.event_queue: Queue[Event] = Queue()
        self.frequency = 1 / fps

        # Create a root element with the size of the terminal resolution
        self._root = Division(style=f"rows={rows}, columns={columns}")
        self.root = self._root

        self.event_broker = EventBroker()

        def show_cursor(event: MouseEvent):
            """Draw cursor and change its position every move event"""
            area = show_cursor.area

            def draw_cursor() -> None:
                try:
                    area[event.coordinates.row][event.coordinates.column] = (
                            colorama.Fore.BLACK + colorama.Back.WHITE +
                            area[event.coordinates.row][event.coordinates.column] +
                            colorama.Style.RESET_ALL
                        )
                except IndexError:
                    pass

            def undraw_cursor() -> None:
                prev_coords = show_cursor.prev_coords
                try:
                    area[prev_coords.row][prev_coords.column] = show_cursor.prev_value
                except IndexError:
                    pass

            prev_value = show_cursor.prev_value
            try:
                prev_value = area[event.coordinates.row][event.coordinates.column]
            except IndexError:
                pass

            draw_cursor()
            undraw_cursor()
            show_cursor.prev_value = prev_value
            show_cursor.prev_coords = event.coordinates

        show_cursor.prev_coords = Coordinates(0, 0)
        show_cursor.prev_value = self._root.area.char_area[0][0]
        show_cursor.area = self._root.area.char_area
        self.event_broker.subscribe(
                event=MouseEventTypes.MOUSE_MOVE,
                subscriber=None,
                post_composition=lambda event: show_cursor(event)
        )

    @property
    def root(self) -> Container:
        """Get the root component"""
        return self._root

    @root.setter
    def root(self, new_root: Container) -> None:
        """Change the root component"""
        self._root = new_root

    def get_events(self) -> None:
        """Continuously fetch events and put them in the event queue."""
        from tui.events._mouse_parser import MouseParser
        from tui.events.key_event import HotkeyEvent
        from tui.events.keys import ANSI_SEQUENCES_KEYS

        while True:
            # read from stdin
            control_code = self.__terminal.read_bytes(bytes=16).decode()
            # check if it's a control sequence or a simple key press
            if len(control_code) == 1:
                self.event_queue.put(HotkeyEvent(control_code))
                continue

            # check if it's a mouse control code and add to the event queue
            try:
                self.event_queue.put(
                        HotkeyEvent(ANSI_SEQUENCES_KEYS[control_code])
                    )
            except KeyError:
                self.event_queue.put(MouseParser.get_mouse_event(control_code))

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
                    pre_composit_hooks, post_composit_hooks = (
                            self.event_broker.handle(event)
                        )
                    print(
                            Compositor.compose(
                                    self.root,
                                    pre_composit=pre_composit_hooks,
                                    post_composit=post_composit_hooks,
                                    event=event),
                            end=''
                        )

                # time.sleep(self.frequency)
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
