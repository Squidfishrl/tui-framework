"""App handles other modules and prints the application to the terminal"""

from __future__ import annotations

import threading
from time import perf_counter
from typing import Optional
from queue import Queue

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
            if rows is None:
                rows = self.__terminal.rows
            if columns is None:
                columns = self.__terminal.columns
        except OSError:
            pass

        self.event_queue: Queue[Event] = Queue()
        self.frequency = 1 / fps

        # Create a root element with the size of the terminal resolution
        self._root = Division(style=f"rows={rows}, columns={columns}")
        self.root = self._root

        def mem_cursor_pos(event: MouseEvent):
            """Helper function for show_cursor - memorizes cursor position"""
            # Subtract 1 because rows and columns start at 1 but arrays do at
            # at 0
            mem_cursor_pos.coords = Coordinates(
                    _row=event.coordinates.row - 1,
                    _column=event.coordinates.column - 1)

        def show_cursor(area: list[list[str]]):
            """Draw cursor and change its position every move event"""

            def draw_cursor() -> None:
                row = mem_cursor_pos.coords.row
                col = mem_cursor_pos.coords.column
                show_cursor.prev_coords = mem_cursor_pos.coords
                try:
                    show_cursor.prev_value = area[row][col]
                    area[row][col] = "\x1b[30;47h" + area[row][col]
                except IndexError:
                    return

            def undraw_cursor() -> None:
                row = show_cursor.prev_coords.row
                col = show_cursor.prev_coords.column
                try:
                    area[row][col] = show_cursor.prev_value
                except IndexError:
                    return

            try:
                undraw_cursor()
            except AttributeError:
                # prev value isn't set on first call
                pass

            try:
                draw_cursor()
            except AttributeError:
                # mem_cursor_pos.coords isn't set before a event occurs
                pass

        self._show_cursor = show_cursor
        EventBroker.subscribe(
                event=MouseEventTypes.MOUSE_MOVE,
                subscriber=None,
                post_composition=mem_cursor_pos
        )

        def set_focus(event: MouseEvent) -> None:
            """Set focus to a component, once it's clicked"""
            focus_component = self.root.find_component(event.coordinates)
            if (focus_component is None or
                    focus_component == set_focus.prev_component):
                return

            set_focus.prev_component._focus = False
            focus_component._focus = True
            set_focus.prev_component = focus_component

        set_focus.prev_component = None
        EventBroker.subscribe(
                event=MouseEventTypes.MOUSE_LEFT_CLICK,
                subscriber=None,
                pre_composition=set_focus
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
            control_code = self.__terminal.read_bytes(_bytes=16).decode()
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
            pre_composit_hook = []
            post_composit_hook = []
            timer_start = perf_counter()
            while True:
                while self.event_queue.qsize() > 0:
                    event = self.event_queue.get()
                    EventBroker.handle(
                            event=event,
                            pre_composit_hook=pre_composit_hook,
                            post_composit_hook=post_composit_hook
                    )

                if perf_counter() - timer_start >= self.frequency:
                    composited_area = Compositor.compose(
                                    self.root,
                                    pre_composit=pre_composit_hook,
                                    post_composit=post_composit_hook)
                    self._show_cursor(composited_area.char_area)
                    self.__terminal.print(composited_area)
                    timer_start = perf_counter()
                    pre_composit_hook = []
                    post_composit_hook = []

        except KeyboardInterrupt:
            self.__terminal.disable_mouse()
            self.__terminal.disable_input()
        except BaseException as e:
            self.__terminal.disable_mouse()
            self.__terminal.disable_input()
            raise e


def main():
    """Run an app"""
    app: App = App(fps=60)
    app.root.add_border(DefaultBorder)
    app.run()


if __name__ == "__main__":
    main()
