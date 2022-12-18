"""App handles other modules and prints the application to the terminal"""

from terminal import Terminal
from area import Area


class App():
    """Contains everything necessary for running the application."""
    def __init__(self) -> None:
        # Instance of the terminal the app is being ran in
        self.__terminal: Terminal = Terminal()
        # 2D array of chars representing terminal resolution
        self.__area: Area = Area(
                rows=self.__terminal.rows,
                columns=self.__terminal.columns
        )

    def run(self) -> None:
        """Start and constantly update the app."""
        while True:
            print(self.__area.char_area)


def main():
    """Run an app"""
    app: App = App()
    app.run()


if __name__ == "__main__":
    main()
