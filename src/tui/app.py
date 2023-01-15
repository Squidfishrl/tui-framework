"""App handles other modules and prints the application to the terminal"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tui.terminal import Terminal

if TYPE_CHECKING:
    from tui.component import Container


class App():
    """Contains everything necessary for running the application."""
    def __init__(self) -> None:
        # Instance of the terminal the app is being ran in
        self.__terminal: Terminal = Terminal()
        self.root: Container  # TODO: Should change to a non abstract class

    def run(self) -> None:
        """Start and constantly update the app."""
        while True:
            pass


def main():
    """Run an app"""
    app: App = App()
    app.run()


if __name__ == "__main__":
    main()
