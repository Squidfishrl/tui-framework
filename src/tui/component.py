"""
The component is the main element of the UI, as everything that's displayed
resides within a component. There are many types of components, varying in
functionality, although they can be separated into 2 groups - containers and
widgets. If you're interested in creating custom user-defined components, you
may want to familiarize yourself with this file.
"""

from __future__ import annotations

from typing import Any, Optional

from tui._coordinates import Coordinates, Rectangle
from tui.area import Area
from tui.component_node import CMNode
from tui.style import Style
from tui.styles.border import Border


class Component(CMNode):
    """Abstract class responsible for creating TUI elements."""
    def __init__(
            self,
            style: str | Style = Style(),  # Style properties for the component
            identifier: Optional[str] = None,  # Unique id
    ) -> None:
        self.style = style
        # if a component has focus, it will listen to it's non-global events
        self._focus = False

        self.__area = Area(self.__style.area_info)

        # rect mapping is the rectangle which this child component resides in,
        # using absolute coordinates (relative to its parent-moost (root)
        # component). We can learn the rect mapping only during composition,
        # hence where it's set.
        self.__rect_mapping: Optional[Rectangle] = None

        super().__init__(identifier=identifier)

    def add_border(self, border: Border) -> None:
        """Add border to the component. Note that adding a border decreases the
        space the component's can use"""
        self.area.add_border(border)

    def set_style(self, attribute_name: str, value: Any) -> None:
        """Change the value of a style attribute"""
        self.style.set_value(attribute_name, value)

    def get_style(self, attribute_name: str) -> Any:
        """Get the value of a style attribute"""
        self.style.get_value(attribute_name)

    def has_focus(self) -> bool:
        """Does the component have focus?"""
        return self._focus

    def find_component(self, coordinates: Coordinates) -> Optional[Component]:
        """Find the child-most component which encapsulates the coordinates we
        search by. A recursive depth search is performed on the component tree.
        """
        # recursion exit condition. It's checked before the for loop to
        # eliminate unnecessary recursion when the mouse is outside the
        # container
        if self._rect_mapping is None or coordinates not in self._rect_mapping:
            return None

        # at this point we know that the coordinates are within this component
        # so a children check is useless since the parent-most component always
        # steal_focus priority
        if self.get_style("steal_focus") is True:
            return self

        for child in self.children:
            child_match = child.find_component(coordinates)

            if child_match is not None:
                return child_match

        return self

    @property
    def _rect_mapping(self) -> Optional[Rectangle]:
        """Get the rectangle (absolute coordinates) this component is mapped
        to. Returns None if component is yet to be mapped."""
        return self.__rect_mapping

    @_rect_mapping.setter
    def _rect_mapping(self, rect: Optional[Rectangle]) -> None:
        """Set the rectangle (absolute coordinates), this component is mapped
        to. Set to None the component isn't mapped. This method should be
        called by the compositor."""
        self.__rect_mapping = rect

    @property
    def style(self) -> Style:
        """Get this component's style"""
        return self.__style

    @style.setter
    def style(self, style: str | Style) -> None:
        """Set the component's style"""
        if isinstance(style, str):
            self.__style = Style.fromstr(style)
        else:
            self.__style = style

    @property
    def area(self) -> Area:
        """Get this component's area (space it's drawn in)"""
        return self.__area

    @area.setter
    def area(self, area: Area) -> None:
        """Get this component's area (space it's drawn in).
        Mainly used for testing.
        """
        self.__area = area
