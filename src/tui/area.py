"""Area for the component when it's rendered"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from tui._area_box_model import BoxModel
from tui._coordinates import RestrictedCoordinates, Coordinates

if TYPE_CHECKING:
    from tui.styles.area import AreaInfo
    from tui.styles.border import Border


class Area:
    """Area for the component when it's rendered
    Defines how the component looks in isolation (without parents)
    """
    # TODO: methods to add margin and padding after initialization
    def __init__(
            self,
            area_info: AreaInfo,  # min, max rows
            border: Optional[Border] = None
    ) -> None:
        self.model = BoxModel(info=area_info)
        self.char_area: list[list[str]] = [  # rows x columns
                [' ' for _ in range(self.columns)]
                for _ in range(self.rows)
            ]

        # used for easier char_area editing.
        self.area_ptr = RestrictedCoordinates(
                    _row=0,
                    _column=0,
                    _restriction=self.model.with_padding,
                    relative=True
                )

        self.add_border(border)

    def add_border(self, border: Optional[Border]) -> None:
        """Apply border to the area"""
        if border is None:
            return

        self.area_ptr.restriction = self.model.with_margin

        border_top = (
                # First row
                border.top_left
                # -2 to account for the corner pieces
                + border.horizontal * (self.model.with_margin.columns - 2)
                + border.top_right
            )

        border_bottom = (
                # Last row
                '\n' + border.bottom_left
                # -2 to account for the corner pieces
                + border.horizontal * (self.model.with_margin.columns - 2)
                + border.bottom_right
            )

        border_side = (
                # Side
                # -2 to account for the corner pieces
                ('\n' + border.vertical) * (self.model.with_margin.rows - 2)
            )

        # Write the border
        self.add_chars(string=border_top)
        self.add_chars(string=border_side, ptr_preserve=False)  # Left side
        self.add_chars(string=border_bottom)
        # Right side (set area pointer at top_right corner of restriction)
        self.area_ptr.row = self.area_ptr.restriction.top_left.row
        self.area_ptr.column = self.area_ptr.restriction.top_right.column
        self.add_chars(string=border_side, column_preserve=True)  # Right side

        # Reset pointer
        self.model._set_border(1, 1, 1, 1)
        self.area_ptr.restriction = self.model.with_padding

    def add_chars(
            self,
            string: str,  # string to be added to the area
            # should new line start at current area pointer column
            column_preserve: bool = False,
            ptr_preserve: bool = True  # reset area pointer to initial position
    ) -> None:
        """Add a string starting from area_ptr. '\n' means row increment
        area_ptr is unaffected
        """

        initital_coords = Coordinates(
                    _row=self.area_ptr.row,
                    _column=self.area_ptr.column
                )

        if not self._verify_str(
                string=string,
                column_preserve=column_preserve
        ):
            raise IndexError("String is too large")

        for count, char in enumerate(string):
            if char == '\n':
                # if area_ptr is on the last row and the last char is a newline
                # area_ptr restriction would activate, hence the latter check
                if count >= len(string) - 1:
                    break

                self.area_ptr.row += 1
                if column_preserve:
                    self.area_ptr.column = initital_coords.column
                else:
                    self.area_ptr.column = (
                            self.area_ptr.restriction.top_left.column
                        )

                continue

            self.char_area[self.area_ptr.row][self.area_ptr.column] = char

            # Required to prevent RestrictedCoordinates exception
            if (self.area_ptr.column < self.area_ptr.restriction.bottom_right
                    .column):
                self.area_ptr.column += 1

        if ptr_preserve:
            self.area_ptr.row = initital_coords.row
            self.area_ptr.column = initital_coords.column
        else:
            # column is incremented one last time after adding the last char
            # this can force area_ptr to go out of bounds
            # FIXME: it still should with no box model
            # hence returning the pointer 1 back
            self.area_ptr.column -= 1

    def _verify_str(self, string: str, column_preserve: bool) -> bool:
        """Verify that string can fit in char_area - used in add_chars"""
        row = self.area_ptr.get_relative_coords().row
        column = self.area_ptr.get_relative_coords().column

        for char in string:
            if char == '\n':
                row += 1
                if column_preserve:
                    column = self.area_ptr.get_relative_coords().column
                else:
                    column = 0  # relative 0 to restriction

                continue

            if (row >= self.area_ptr.restriction.rows or
                    column >= self.area_ptr.restriction.columns):
                return False

            column += 1

        return True

    def __str__(self):
        return "\n".join(
                ["".join(list(row)) for row in self.char_area]
            )

    @property
    def rows(self) -> int:
        """Get the rows in the area"""
        return self.model.info.rows

    @property
    def columns(self) -> int:
        """Get the columns in the area"""
        return self.model.info.columns

    @rows.setter
    def rows(self, rows: int) -> None:
        """Set the rows in the area"""
        raise NotImplementedError

    @columns.setter
    def columns(self, columns: int) -> None:
        """Set the columns in the area"""
        raise NotImplementedError
