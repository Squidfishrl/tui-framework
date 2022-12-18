"""Abstract class for creating TUI elements"""

from __future__ import annotations

from component_node import CMNode


class Component(CMNode):
    """Abstract class for creating TUI elements"""

    def __init__(
            self,
            *children: Component,  # This component's child components
            identifier: str | None = None,  # Unique identifier
    ) -> None:

        self._size = (0, 0)
        super().__init__(identifier)

        for child in children:
            self.children.append(child)

    def get_id(self) -> str | None:
        """Get the component's id"""
        return self._id
