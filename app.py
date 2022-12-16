"""App handles other modules and prints the application to the terminal"""

from terminal import Terminal


class App():
    """Contains everything necessary for running the application.

    __terminal - Terminal:
        The instance of the terminal the app is being ran in.
    __stdout_buffer - list[list[str]]:
        A 2D array of chars - __stdout_buffer[row][column].
        Size is equal to terminal resolution.
    """
    def __init__(self) -> None:
        self.__terminal: Terminal = Terminal()
        self.__stdout_buffer: list[list[str]] = [
                [' ' for _ in range(self.__terminal.columns)]
                for _ in range(self.__terminal.rows)
        ]

    def run(self):
        """Start and constantly update the app."""
        while True:
            print(self.__stdout_buffer)


def main():
    """Run an app"""
    app: App = App()
    app.run()


if __name__ == "__main__":
    main()
