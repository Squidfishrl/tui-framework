"""
This file makes the connection between the application and the terminal it's
being ran it.
"""

from os import get_terminal_size, terminal_size, system, read
from sys import stdin
from typing import Optional, TextIO


class Terminal:
    """Responsible for providing an interface to the terminal the program is
    being ran in"""

    def __init__(self, input_stream: TextIO = stdin) -> None:
        self.__size: terminal_size = get_terminal_size()  # columns and rows
        self.input_stream = input_stream
        self.input_fd = input_stream.fileno()  # save fd in case it's lost

        self.__mouse_input = False
        self.__input = False

        self._prev_state: Optional[str] = None

        self.enable_input()
        self.enable_mouse()

    def print(self, string: str) -> None:
        """Print a string to the terminal. Overwrites content in the terminal
        for higher response time and no stuttering."""
        # handle first print
        if self._prev_state is None:
            print(string, end="", flush=True)
            self._prev_state = string
            return

        print(self._mutate_on_diff(self._prev_state, string),
              end="",
              flush=True)
        self._prev_state = string

    def _mutate_on_diff(self, str1: str, str2: str) -> str:
        """Find the difference between 2 strings and return a string which
        describes how the first one should change to become the second. Assume
        that both strings have the same dimensions. Expected strings are
        unnecessarily bloated for this sole reason (a lot of whitespaces can be
        followed by '\n') """
        # TODO: use a string stream instead (optimization)
        mutate_str = ""
        # -1 since it will be incremented for the first char and we want
        # (0,0) to be top left
        column = -1
        row = 0

        # are the char differences consecutive
        streak = False

        for count, char1 in enumerate(str1):
            char2 = str2[count]

            if char2 == '\n':
                column = 0
                row += 1
            else:
                column += 1

            if char1 != char2:
                if streak is False:
                    # move cursor
                    mutate_str += self._move_cursor(row=row, column=column)
                    streak = True

                mutate_str += char2
            else:
                streak = False

        return mutate_str

    def _move_cursor(self, row: int, column: int) -> str:
        """Return an ANSI code which moves the string to the specified
        coordinates."""
        return f"\x1b[{row};{column}f"

    def read_bytes(self, _bytes: int = 16) -> bytes:
        """Read bytes from the input stream"""
        return read(self.input_fd, _bytes)

    def enable_mouse(self) -> None:
        """Enable mouse reporting"""
        if self.input is False:
            raise ValueError("Input is disabled, cannot enable mouse input")

        print("\x1b[?1000;1003;1006;1015h")
        self.__mouse_input = True

    def disable_mouse(self) -> None:
        """Disable mouse reporting"""
        print("\x1b[?1000;1003;1006;1015l")
        self.__mouse_input = False

    def enable_input(self) -> None:
        """Change terminal settings to preferred ones. Call disable input to
        revert them."""
        system("stty -icanon")  # Enable shell input
        system("stty -echo")  # Disable character printing on stdin
        self.__input = True

    def disable_input(self) -> None:
        """Restore terminal settings so that they do not affect the terminal
        after the app terminates."""
        system("stty echo")
        system("stty sane")
        self.__input = False

    @property
    def input(self) -> bool:
        """Is input enabled?"""
        return self.__input

    @property
    def mouse_input(self) -> bool:
        """Is mouse input enabled?"""
        return self.__mouse_input

    @property
    def columns(self) -> int:
        """Return the amount of visible columns in the terminal."""
        return self.__size[0]

    @property
    def rows(self) -> int:
        """Return the amount of visible rows in the terminal."""
        return self.__size[1]


if __name__ == '__main__':
    term: Terminal = Terminal()
    print(f"Size: {term.rows};{term.columns}")
