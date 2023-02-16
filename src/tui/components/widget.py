"""
The widget is an abstract component which cannot have child components. It can
override the default response to most events and should focus on providing some
functionality. Some examples of pure widgets are - labels, buttons and input
fields. If you're looking to define custom widgets, you may need to inherit
from both the Widget and the Container class. An example would be bundling
2 input fields and a button inside a division to make a 'login form'.
"""

from abc import abstractmethod
from typing import Optional

from tui.component import Component
from tui.style import Style


class Widget(Component):
    """An abstract component that can't hold other components and can override
    signal behaviour."""
    def __init__(
            self,
            style: str | Style = Style(),  # Style properties for the component
            identifier: Optional[str] = None,  # Unique identifier
    ) -> None:
        super().__init__(identifier=identifier, style=style)

    @abstractmethod
    def _render_to_area(self) -> None:
        """Render the component's content to its area"""

    @property
    def children(self) -> None:
        """Widgets can't have child components"""
        return None
