"""Area for the component when it's rendered"""

from tui.style import AreaInfo


class Area:
    """Area for the component when it's rendered"""
    def __init__(
            self,
            area_info: AreaInfo  # min, max rows
    ) -> None:
        self._rows: int = area_info.min_rows
        self._columns: int = area_info.min_columns
        self.char_area: list[list[str]]
        self.update_area()

    def update_area(self) -> None:
        """Update the area to match rows x columns resolution"""
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
