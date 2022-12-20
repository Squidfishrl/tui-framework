"""Abstract class for creating TUI elements"""

from __future__ import annotations

from tui.area import Area
from tui.component_node import CMNode
from tui.style import Style


class Component(CMNode):
    """Abstract class for creating TUI elements"""
    def __init__(
            self,
            identifier: str | None = None,  # Unique identifier
            style: Style = Style()  # Style properties for the component
    ) -> None:
        self.__style = style
        self.__area = Area(self.__style.area_info)
        super().__init__(identifier)

    @property
    def style(self) -> Style:
        """Get this component's style"""
        return self.__style

    @property
    def area(self) -> Style:
        """Get this component's area (space it's drawn in)"""
        return self.__area
