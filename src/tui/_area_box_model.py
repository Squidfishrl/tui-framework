"""
The area box model tells the area within what rectangular bounds should the
component's content be placed in. The box model is entirely similar to the CSS
box model:

    Area
    +--------------------------------------------------------+
    |                                                        |
    |    Margin                                              |
    |    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    |
    |    x                                              x    |
    |    x    Border                                    x    |
    |    x    ╔════════════════════════════════════╗    x    |
    |    x    ║  Padding                           ║    x    |
    |    x    ║  ++++++++++++++++++++++++++++++++  ║    x    |
    |    x    ║  +                              +  ║    x    |
    |    x    ║  +                              +  ║    x    |
    |    x    ║  +          Content             +  ║    x    |
    |    x    ║  +                              +  ║    x    |
    |    x    ║  +                              +  ║    x    |
    |    x    ║  ++++++++++++++++++++++++++++++++  ║    x    |
    |    x    ║                                    ║    x    |
    |    x    ╚════════════════════════════════════╝    x    |
    |    x                                              x    |
    |    x                                              x    |
    |    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    |
    |                                                        |
    |                                                        |
    +--------------------------------------------------------+

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tui._coordinates import Coordinates, Rectangle

if TYPE_CHECKING:
    from tui.styles.area import AreaInfo


class BoxModel:
    """Responsible for defining the Area Box Model (as multiple rectangles
    nested within each-other) and handling dynamic changes to it."""
    # TODO: methods for updating margin and padding
    def __init__(self, info: AreaInfo) -> None:
        self.info = info

        # Entire area
        self.area_rect: Rectangle = Rectangle(
                top_left=Coordinates(0, 0),
                bottom_right=Coordinates(
                        _row=info.rows - 1,
                        _column=info.columns - 1
                    )
            )

        # Accessible area after margin is applied
        self.with_margin: Rectangle = self.area_rect.inner_rect(
                    top_offset=info.margin_top,
                    bottom_offset=info.margin_bottom,
                    left_offset=info.margin_left,
                    right_offset=info.margin_right
                )

        # Accessible area after border is applied
        self.with_border: Rectangle = self.with_margin.inner_rect(0, 0, 0, 0)

        # Accessible area after padding is applied
        self.with_padding: Rectangle = self.with_border.inner_rect(
                    top_offset=info.padding_top,
                    bottom_offset=info.padding_bottom,
                    left_offset=info.padding_left,
                    right_offset=info.padding_right
                )

    def _set_border(
            self,
            left_offset: int,
            right_offset: int,
            top_offset: int,
            bottom_offset: int
    ) -> None:
        """Update box model when adding/changing border."""
        self.with_border: Rectangle = self.with_margin.inner_rect(
                    left_offset=left_offset,
                    right_offset=right_offset,
                    top_offset=top_offset,
                    bottom_offset=bottom_offset
                )

        # Apply padding as well (area might not be large enough)
        self.with_padding: Rectangle = self.with_border.inner_rect(
                    top_offset=self.info.padding_top,
                    bottom_offset=self.info.padding_bottom,
                    left_offset=self.info.padding_left,
                    right_offset=self.info.padding_right
                )
