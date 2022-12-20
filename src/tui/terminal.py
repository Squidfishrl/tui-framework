"""Terminal module allows reading and modifying the terminal's properties"""

from os import get_terminal_size, terminal_size


class Terminal:
    """Useful information about the terminal that's currently being used."""

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
