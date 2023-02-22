"""
This file makes the connection between the application and the terminal it's
being ran it.
"""

from os import get_terminal_size, terminal_size, system, read
from sys import stdin
from typing import TextIO


class Terminal:
    """Responsible for providing an interface to the terminal the program is
    being ran in"""

    def __init__(self, input_stream: TextIO = stdin) -> None:
        self.__size: terminal_size = get_terminal_size()  # columns and rows
        self.input_stream = input_stream
        self.input_fd = input_stream.fileno()  # save fd in case it's lost

        self.__mouse_input = False
        self.__input = False

        self.enable_input()
        self.enable_mouse()

    def read_bytes(self, bytes: int = 16) -> bytes:
        """Read bytes from the input stream"""
        return read(self.input_fd, bytes)

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
