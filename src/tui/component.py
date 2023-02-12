"""Abstract class for creating TUI elements"""

from __future__ import annotations

from typing import Any, Optional

from tui.area import Area
from tui.component_node import CMNode
from tui.style import Style
from tui.styles.border import Border


class Component(CMNode):
    """Abstract class for creating TUI elements"""
    def __init__(
            self,
            identifier: Optional[str] = None,  # Unique identifier
            name: Optional[str] = None,  # Component's name (for debug)
            style: str | Style = Style()  # Style properties for the component
    ) -> None:
        if isinstance(style, str):
            self.__style = Style.fromstr(style)
        else:
            self.__style = style

        self.__area = Area(self.__style.area_info)
        super().__init__(identifier=identifier, name=name)

    def add_border(self, border: Border) -> None:
        """Add border to the component"""
        self.area.add_border(border)

    def set_style(self, attribute_name: str, value: Any) -> None:
        """Change the value of a style attribute"""
        self.style.set_value(attribute_name, value)

    def get_style(self, attribute_name: str) -> Any:
        """Get the value of a style attribute"""
        self.style.get_value(attribute_name)

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
