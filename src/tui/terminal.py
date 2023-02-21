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
        self._prepare()

    def read_bytes(self, bytes: int = 16) -> bytes:
        """Read bytes from the input stream"""
        return read(self.input_fd, bytes)

    def _prepare(self) -> None:
        """Change terminal settings to preferred ones. Call _restore to revert
        them."""
        system("stty -icanon")  # Enable shell input
        system("stty -echo")  # Disable character printing on stdin

    def _restore(self) -> None:
        """Restore terminal settings so that they do not affect the terminal
        after the app terminates."""
        system("stty echo")

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
