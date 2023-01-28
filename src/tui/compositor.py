"""Composes all components to one area"""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from tui._coordinates import Coordinates, Rectangle, CoordinateError
from tui.component import Area

if TYPE_CHECKING:
    from tui.component import Component


class CompositorError(Exception):
    """Base class for exceptions in the compositor"""


class InsufficientAreaError(CompositorError):
    """Raise when components can't be composed because their area size isn't
    large enough"""


class Compositor:
    """Composes all components to one area
    Handle all modifications to 'Area'
    """

    @staticmethod
    def compose(root: Component) -> Area:
        """Compose a component with its children components recursively

        root: the component's area that's being composed
        next_component: rectangular area which the next component should occupy
        """

        new_area = copy.deepcopy(root.area)

        # the rectanhle the previous child was in
        prev_rect: None | Rectangle = None

        for child in root.children:
            try:
                prev_rect = Compositor._get_next_rectangle(
                        parent=root,
                        prev_rect=prev_rect,
                        component=child
                    )
            except CoordinateError as exc:
                raise InsufficientAreaError(
                        "Component area isn't large enough"
                    ) from exc

            # recursion ends when there are no more children
            child_area = Compositor.compose(child)
            new_area.area_ptr.row = prev_rect.top_left.row
            new_area.area_ptr.column = prev_rect.top_left.column

            # draw child component
            try:
                new_area.add_chars(str(child_area), column_preserve=True)
            except IndexError as exc:
                raise InsufficientAreaError(
                        "Component area isn't large enough"
                    ) from exc

        return new_area

    @staticmethod
    def _get_next_rectangle(
            parent: Component,  # the parent component this one will reside in
            component: Component,  # the component calculations are done for
            prev_rect: None | Rectangle = None  # rect for the prev component
    ) -> Rectangle:
        """Helper function that decides where components are placed when
        compositioning"""
        if parent.style.compositor_info.inline:
            return Compositor.__get_next_rectangle_inline(
                    parent=parent,
                    component=component,
                    prev_rect=prev_rect
                )

        return Compositor.__get_next_rectangle_block(
                parent=parent,
                component=component,
                prev_rect=prev_rect
            )

    @staticmethod
    def __get_next_rectangle_inline(
            parent: Component,  # the parent component this one will reside in
            component: Component,  # the component calculations are done for
            prev_rect: None | Rectangle = None  # rect for the prev component
    ) -> Rectangle:
        """Helper function for inline compositing. Returns the area the next
        component should be placed in

        Default prev_rectangle is a rectangle outside of the parent's area
        that's derrived to place the component in the top left of the parent
        component's area:
            top_left:  row = 0 && column <= -1
            bottom_right:  row >= 0 && column = -1
        """
        if prev_rect is None:
            prev_rect = Rectangle(
                    top_left=Coordinates(_row=0, _column=-1),
                    bottom_right=Coordinates(_row=0, _column=-1)
                )

        return Rectangle(
                top_left=Coordinates(
                        _row=prev_rect.top_left.row,
                        _column=prev_rect.bottom_right.column + 1
                    ),
                bottom_right=Coordinates(
                        _row=parent.area.rows - 1,
                        _column=prev_rect.bottom_right.column +
                        component.area.columns
                    )
            )

    @staticmethod
    def __get_next_rectangle_block(
            parent: Component,  # the parent component this one will reside in
            component: Component,  # the component calculations are done for
            prev_rect: None | Rectangle = None  # rect for the prev component
    ) -> Rectangle:
        """Helper function for block compositing. Returns the area the next
        component should be placed in

        Default prev_rectangle is a rectangle outside of the parent's area
        that's derrived to place the component in the top left of the parent
        component's area:
            top_left:  row = -1 && column <= 0
            bottom_right:  row >= -1 && column = 0
        """
        if prev_rect is None:
            prev_rect = Rectangle(
                    top_left=Coordinates(_row=-1, _column=0),
                    bottom_right=Coordinates(_row=-1, _column=0)
                )

        return Rectangle(
                top_left=Coordinates(
                        _row=prev_rect.bottom_right.row + 1,
                        _column=prev_rect.top_left.column
                    ),
                bottom_right=Coordinates(
                        _row=prev_rect.bottom_right.row + component.area.rows,
                        _column=parent.area.columns - 1
                    )
            )

    @staticmethod
    def fill_area(component: Component, symbol: str) -> Area:
        """Fill the entire area of a component with a symbol"""
        if len(symbol) != 1:
            raise ValueError("symbol must be one char")

        new_area = copy.deepcopy(component.area)
        new_area.area_ptr.row = 0
        new_area.area_ptr.column = 0

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
        new_area.area_ptr.row = 0
        new_area.area_ptr.column = 0

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
        new_area.area_ptr.row = new_area.rows - 1
        new_area.area_ptr.column = 0
        new_area.add_chars(symbol * new_area.rows)
        return new_area
