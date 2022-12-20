"""Abstract class for creating TUI elements"""

from __future__ import annotations

from typing import TYPE_CHECKING
from tui.area import Area
from tui.component_node import CMNode
from tui.style import Style


class Component(CMNode):
    """Abstract class for creating TUI elements"""
    def __init__(
            self,
            identifier: str | None = None,  # Unique identifier
            name: str | None = None,  # Component's name (for debug)
            style: Style = Style()  # Style properties for the component
    ) -> None:
        self.__style = style
        self.__area = Area(self.__style.area_info)
        super().__init__(identifier=identifier, name=name)

    @property
    def style(self) -> Style:
        """Get this component's style"""
        return self.__style

    @property
    def area(self) -> Style:
        """Get this component's area (space it's drawn in)"""
        return self.__area
