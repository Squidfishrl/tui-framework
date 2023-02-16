"""
This file makes the connection between the application and the terminal it's
being ran it.
"""

from os import get_terminal_size, terminal_size


class Terminal:
    """Responsible for providing an interface to the terminal the programm is
    being ran in"""

    def __init__(self) -> None:
        self.__size: terminal_size = get_terminal_size()  # columns and rows

    @property
    def columns(self) -> int:
        """Return the amount of visible columns in the terminal"""
        return self.__size[0]

    @property
    def rows(self) -> int:
        """Return the amount of visible rows in the terminal"""
        return self.__size[1]


if __name__ == '__main__':

    term: Terminal = Terminal()
    print(f"Size: {term.rows};{term.columns}")
