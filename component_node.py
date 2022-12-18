"""Node definition creating a DOM-like structure"""

from _node_list import NodeList
from component import Component


class CMNode:
    """Base object in the model"""

    def __init__(
            self,
            identifier: str | None = None,  # unique id for the node
            name: str | None = None  # for debug readability
    ) -> None:
        self._id = identifier
        self._name = name
        self.children: NodeList[Component] = NodeList()

    def get_id(self) -> str | None:
        """Get the id of the node"""
        return self._id

    def get_name(self) -> str | None:
        """Get the name of this node"""
        return self._name
