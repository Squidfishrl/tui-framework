"""Abstract component that can't hold other components and should focus on
functionality - a button, label..
"""

from tui.component import Component
from tui.style import Style


class Widget(Component):
    """Abstract component that can't hold other components"""
    def __init__(
            self,
            identifier: str | None = None,  # Unique identifier
            style: str | Style = Style()  # Style properties for the component
    ) -> None:
        super().__init__(identifier=identifier, style=style)

    @property
    def children(self) -> None:
        """Widgets can't have child components"""
        return None
