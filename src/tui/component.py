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
            name: str | None = None,  # Component's name (for debug)
            style: str | Style = Style()  # Style properties for the component
    ) -> None:
        if isinstance(style, str):
            self.__style = Style.fromstr(style)
        else:
            self.__style = style

        self.__area = Area(self.__style.area_info)
        super().__init__(identifier=identifier, name=name)

    @property
    def style(self) -> Style:
        """Get this component's style"""
        return self.__style

    @property
    def area(self) -> Area:
        """Get this component's area (space it's drawn in)"""
        return self.__area

    @area.setter
    def _area(self, area: Area) -> None:
        """Set the area of an object. The previous area's contents are copied
        to the new area"""
        # TODO: copy the contents of the old area to the new area
        self.__area = area

    def _add_border(self) -> None:
        pass
