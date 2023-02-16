"""
The container is an abstract component solely responsible for have child
components. It manages the order they are composited in as well as
the position they appear in. Examples of containers are Divisions and
Grids. If you're looking to define custom components, you're advised to take a
look at the Widget class before you do so.
"""

from typing import Optional
from tui.component import Component
from tui.style import Style


class Container(Component):
    """
    Abstract component that's responsible for containing and organizing other
    components.
    `@property def children(self)` should be implemented in child classes
    """

    def __init__(
            self,
            style: str | Style = Style(),  # Style properties for the component
            identifier: Optional[str] = None,  # Unique identifier
            *children: Component  # Child components
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
