"""Handle a 2d char matrix with the area box model specification"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tui._coordinates import Coordinates, Rectangle

if TYPE_CHECKING:
    from tui.styles.area import AreaInfo


class BoxModel:
    """
    Layout model for the area
    Defines how the component looks like in isolation

    Area Box Model:

    Area
    +--------------------------------------------------------+
    |    Margin                                              |
    |    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    |
    |    x    Border                                    x    |
    |    x    ╔════════════════════════════════════╗    x    |
    |    x    ║  Padding                           ║    x    |
    |    x    ║  ++++++++++++++++++++++++++++++++  ║    x    |
    |    x    ║  + Content                      +  ║    x    |
    |    x    ║  +                              +  ║    x    |
    |    x    ║  +                              +  ║    x    |
    |    x    ║  +                              +  ║    x    |
    |    x    ║  ++++++++++++++++++++++++++++++++  ║    x    |
    |    x    ║                                    ║    x    |
    |    x    ╚════════════════════════════════════╝    x    |
    |    x                                              x    |
    |    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    |
    |                                                        |
    +--------------------------------------------------------+

    """
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
                    left_offset=info.margin_right,
                    right_offset=info.margin_right
                )

        # Accessible area after border is applied

        # TODO: check if area should have a border
        # self.with_border: Rectangle = self.with_margin.inner_rect(1,1,1,1)
        self.with_border: Rectangle = self.with_margin.inner_rect(0, 0, 0, 0)

        # Accessible area after padding is applied
        self.with_padding: Rectangle = self.with_border.inner_rect(
                    top_offset=info.padding_top,
                    bottom_offset=info.padding_bottom,
                    left_offset=info.padding_left,
                    right_offset=info.padding_right
                )
