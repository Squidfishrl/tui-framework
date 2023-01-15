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
            # Components that inherit Container could pass *children to
            # super().__init__() which is seen as an empty tuple here
            if isinstance(child, tuple):
                continue

            self.append_child(child)

    def append_child(self, component: Component):
        """Add a child at the end of the component list of the container"""
        self.children.append(component)
