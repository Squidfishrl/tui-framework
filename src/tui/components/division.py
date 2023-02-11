"""Container component acting as a diision"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from tui.components.container import Container
from tui.style import Style

if TYPE_CHECKING:
    from tui.component import Component


class Division(Container):
    """Container component acting as a div"""
    def __init__(
            self,
            *children: Component,  # Child components
            identifier: Optional[str] = None,  # Unique identifier
            style: str | Style = Style()  # Style properties for the component
    ) -> None:
        super().__init__(
                children,
                identifier=identifier,
                style=style
            )

    @property
    def children(self):
        return super().children
