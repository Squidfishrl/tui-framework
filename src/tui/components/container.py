"""Abstract component that contains other components"""

from tui.component import Component
from tui.style import Style


class Container(Component):
    """Abstract component that contains and organises other components
    `@property def children(self)` shoould be implemented in child classes
    """

    def __init__(
            self,
            *children: Component,  # Child components
            identifier: str | None = None,  # Unique identifier
            style: Style = Style()  # Style properties for the component
    ) -> None:
        super().__init__(identifier=identifier, style=style)

        for child in children:
            self.children.append(child)
