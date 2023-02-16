"""A division is a container with vertical orientation"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from tui.components.container import Container
from tui.style import Style

if TYPE_CHECKING:
    from tui.component import Component


class Division(Container):
    """A container with vertical (block) orientation"""
    def __init__(
            self,
            style: str | Style = Style(),  # Style properties for the component
            identifier: Optional[str] = None,  # Unique identifier
            *children: Component  # Child components
    ) -> None:
        super().__init__(
                identifier=identifier,
                style=style,
                *children
            )

    @property
    def children(self):
        return super().children
