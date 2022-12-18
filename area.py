"""Area for the component when it's rendered"""


class Area:
    """Area for the component when it's rendered"""
    def __init__(
            self,
            rows: int = 0,  # Rows for the area
            columns: int = 0  # Columns for the area
    ) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.char_area: list[list[str]]
        self.update_area()

    def update_area(self) -> None:
        """Update the area to match rowsXcolumns resolution"""
        self.char_area = [
                [' ' for _ in range(self._columns)]
                for _ in range(self._rows)
            ]

    def get_rows(self) -> int:
        """Get the rows in the area"""
        return self._rows()

    def get_columns(self) -> int:
        """Get the columns in the area"""
        return self._columns()

    def set_rows(self, rows: int) -> None:
        """Set the rows in the area"""
        if rows < 0:
            raise ValueError("Rows cannot be negative")

        self._rows = rows

    def set_columns(self, columns: int) -> None:
        """Set the columns in the area"""
        if columns < 0:
            raise ValueError("Columns cannot be negative")

        self._columns = columns
