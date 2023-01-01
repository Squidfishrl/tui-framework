"""Composes all components to one area"""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from tui.component import Area
from tui._coordinates import Coordinates, Rectangle
from tui.style import AreaInfo

if TYPE_CHECKING:
    from tui.component import Component


class Compositor:
    """Composes all components to one area
    Handle all modifications to 'Area'
    """

    @staticmethod
    def compose(
            root: Component,
            next_component: Rectangle = None
        ) -> Area:
        """Compose a component with its children components recursively

        root: the component's area that's being composed
        next_component: rectangular area which the next component should occupy
        """
        # initialise starting area for first component (its area size)
        if next_component is None:
            max_rows = root.area.rows - 1  # -1 since coords start from 0
            max_cols = root.area.columns - 1
            next_component = Rectangle(
                    Coordinates(0, 0),
                    Coordinates(row=max_rows, column=max_cols)
                )

        # recursion end case
        if root is None:
            return root.area

        new_area = copy.deepcopy(root.area)

        for child in root.children:
            child_area = Compositor.compose(child)

            new_area.area_ptr = next_component.top_left
            new_area.add_chars(str(child_area), column_preserve=True)
            # Assume all components are not inline
            next_component.top_left = Coordinates(
                    row=next_component.top_left.row + child_area.rows,
                    column=next_component.top_left.column
                )
                

        return new_area

    @staticmethod
    def fill_area(component: Component, symbol: str) -> Area:
        """Fill the entire area of a component with a symbol"""
        if len(symbol) != 1:
            raise ValueError("symbol must be one char")

        new_area = copy.deepcopy(component.area)
        new_area.area_ptr = Coordinates(0, 0)

        new_area.add_chars(((symbol * new_area.columns)+"\n") * new_area.rows)
        return new_area

    @staticmethod
    def draw_border(component: Component, symbol: str) -> Area:
        """Draw border around a component
        TODO: Border style should be defined in style.py
        """
        if len(symbol) != 1:
            raise ValueError("symbol must be one char")

        new_area = copy.deepcopy(component.area)
        new_area.area_ptr = Coordinates(0, 0)

        # add first row
        new_area.add_chars(symbol * new_area.rows)

        # add border on the side
        new_area.add_chars(
                (symbol+"\n") * new_area.columns,
                column_preserve=True
            )

        new_area.area_ptr.column = new_area.columns - 1
        new_area.add_chars(
                (symbol+"\n") * new_area.columns,
                column_preserve=True
            )

        # add last row
        new_area.area_ptr = Coordinates(new_area.rows - 1, 0)
        new_area.add_chars(symbol * new_area.rows)
        return new_area

