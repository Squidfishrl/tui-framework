"""Container component acting as a div"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tui.components.container import Container
from tui.style import Style

if TYPE_CHECKING:
    from tui.component import Component


class Division(Container):
    """Container component acting as a div"""
    def __init__(
            self,
            *children: Component,  # Child components
            identifier: str | None = None,  # Unique identifier
            style: Style = Style()  # Style properties for the component
    ) -> None:
        super().__init__(
                children,
                identifier=identifier,
                style=style
            )

    @property
    def children(self):
        return super().children