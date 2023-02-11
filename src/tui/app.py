"""App handles other modules and prints the application to the terminal"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from tui.compositor import Compositor
from tui.styles.border import DefaultBorder
from tui.terminal import Terminal
from tui.components.division import Division

if TYPE_CHECKING:
    from tui.component import Container


class App():
    """Contains everything necessary for running the application."""
    def __init__(
            self,
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

        # Create a root element with the size of the terminal resolution
        self.root = Division(style=f"rows={rows}, columns={columns}")

    def run(self) -> None:
        """Start and constantly update the app."""
        print(Compositor.compose(self.root), end='')
        while True:
            pass


def main():
    """Run an app"""
    app: App = App()
    app.root.add_border(DefaultBorder)
    app.run()


if __name__ == "__main__":
    main()
