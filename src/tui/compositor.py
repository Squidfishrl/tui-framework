"""
The compositor handles combining (compositing) components to a single screen.
It may composite only a part of the screen where updates have occurred.
"""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional

from tui._coordinates import Coordinates, Rectangle, CoordinateError
from tui.component import Area
from tui.events.event_listener import Callback
from tui.styles.compositor import Orientation

if TYPE_CHECKING:
    from tui.component import Component


class CompositorError(Exception):
    """Base class for exceptions in the compositor"""


class InsufficientAreaError(CompositorError):
    """Raise when components can't be composed because their area size isn't
    large enough"""


class Compositor:
    """Responsible for compositing components into a single area"""

    @staticmethod
    def compose(
            root: Component,  # the component which's area is being composed
            pre_composit: list[Callback],
            post_composit: list[Callback]
    ) -> Area:
        """Compose a component with its children components recursively. Run
        pre-compose and post-compose hooks
        """
        for callback in pre_composit:
            callback()

        # set root rect mapping to itself
        # add 1 because area model rect starts at 0
        root._rect_mapping = Rectangle(
                top_left=root.area.model.area_rect.top_left
                + Coordinates(1, 1),
                bottom_right=root.area.model.area_rect.bottom_right
                + Coordinates(1, 1)
            )

        new_area = Compositor._compose(root=root)

        for callback in post_composit:
            callback()

        return new_area

    @staticmethod
    def _compose(root: Component) -> Area:
        """Compose a component with its children components recursively

        root: the component's area that's being composed
        next_component: rectangular area which the next component should occupy
        """

        new_area = copy.deepcopy(root.area)

        # the rectangle the previous child was in
        prev_rect: Optional[Rectangle] = None
        prev_component: Optional[Component] = None

        for child in root.children:
            try:
                prev_rect = Compositor._get_next_rectangle(
                        parent=root,
                        prev_rect=prev_rect,
                        component=child,
                        prev_component=prev_component
                    )

            except CoordinateError as exc:
                raise InsufficientAreaError(
                        "Component area isn't large enough"
                    ) from exc

            # recursion ends when there are no more children
            child_area = Compositor._compose(child)
            prev_component = child
            new_area.area_ptr.row = (
                prev_rect.top_left.row
                + new_area.model.with_padding.top_left.row
            )
            new_area.area_ptr.column = (
                prev_rect.top_left.column
                + new_area.model.with_padding.top_left.column
            )

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
            prev_rect: Optional[Rectangle] = None,
            prev_component: Optional[Component] = None
    ) -> Rectangle:
        """Helper function that decides where components are placed when
        compositing"""
        if parent.style.compositor_info.display == Orientation.INLINE:
            return Compositor.__get_next_rectangle_inline(
                    parent=parent,
                    component=component,
                    prev_rect=prev_rect,
                    prev_component=prev_component
                )

        return Compositor.__get_next_rectangle_block(
                parent=parent,
                component=component,
                prev_rect=prev_rect,
                prev_component=prev_component
            )

    @staticmethod
    def __get_next_rectangle_inline(
            parent: Component,  # the parent component this one will reside in
            component: Component,  # the component calculations are done for
            # rectangle for the previous component
            prev_rect: Optional[Rectangle] = None,
            prev_component: Optional[Component] = None
    ) -> Rectangle:
        """Helper function for inline compositing. Returns the area the next
        component should be placed in

        Default prev_rectangle is a rectangle outside of the parent's area
        that's derived to place the component in the top left of the parent
        component's area:
            top_left:  row = 0 && column <= -1
            bottom_right:  row >= 0 && column = -1
        """

        if prev_component is None and parent._rect_mapping is not None:
            tl = Coordinates(
                        _row=parent._rect_mapping.top_left.row
                        + (parent.area.model.area_rect.rows
                           - parent.area.model.with_padding.rows) - 1,
                        _column=parent._rect_mapping.top_left.column
                        + (parent.area.model.area_rect.columns
                           - parent.area.model.with_padding.columns) - 1
                    )
            br = Coordinates(
                        _row=tl._row + component.area.rows - 1,
                        _column=tl._column + component.area.columns - 1
                    )

            component._rect_mapping = Rectangle(top_left=tl, bottom_right=br)

        elif (prev_component is not None
                and prev_component._rect_mapping is not None):
            tl = Coordinates(
                        _row=prev_component._rect_mapping.top_left.row,
                        _column=prev_component._rect_mapping.bottom_right
                                                            .column + 1
                    )
            br = Coordinates(
                        _row=tl._row + component.area.rows - 1,
                        _column=tl._column + component.area.columns - 1
                    )

            component._rect_mapping = Rectangle(top_left=tl, bottom_right=br)

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
            # rectangle for the previous component
            prev_rect: Optional[Rectangle] = None,
            prev_component: Optional[Component] = None
    ) -> Rectangle:
        """Helper function for block compositing. Returns the area the next
        component should be placed in

        Default prev_rectangle is a rectangle outside of the parent's area
        that's derived to place the component in the top left of the parent
        component's area:
            top_left:  row = -1 && column <= 0
            bottom_right:  row >= -1 && column = 0
        """
        if prev_component is None and parent._rect_mapping is not None:
            tl = Coordinates(
                        _row=parent._rect_mapping.top_left.row
                        + (parent.area.model.area_rect.rows
                           - parent.area.model.with_padding.rows) - 1,
                        _column=parent._rect_mapping.top_left.column
                        + (parent.area.model.area_rect.columns
                           - parent.area.model.with_padding.columns) - 1
                    )
            br = Coordinates(
                        _row=tl._row + component.area.rows - 1,
                        _column=tl._column + component.area.columns - 1
                    )

            component._rect_mapping = Rectangle(top_left=tl, bottom_right=br)
        elif (prev_component is not None
                and prev_component._rect_mapping is not None):
            tl = Coordinates(
                        _row=prev_component._rect_mapping.bottom_right.row + 1,
                        _column=prev_component._rect_mapping.top_left.column
                    )
            br = Coordinates(
                        _row=tl._row + component.area.rows - 1,
                        _column=tl._column + component.area.columns - 1
                    )

            component._rect_mapping = Rectangle(top_left=tl, bottom_right=br)

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
        """Fill the entire area of a component with a symbol. Used mainly for
        debugging and tests"""
        if len(symbol) != 1:
            raise ValueError("symbol must be one char")

        new_area = copy.deepcopy(component.area)
        new_area.area_ptr.row = 0
        new_area.area_ptr.column = 0

        new_area.add_chars(((symbol * new_area.columns)+"\n") * new_area.rows)
        return new_area
