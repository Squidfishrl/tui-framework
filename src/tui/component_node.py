"""
Component nodes are a part of a tree structure, which is very DOM-like. Each
node may have a unique id and any amount of children. Every component should
inherit the Component node class, with the root component being the head of the
tree.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from tui._node_list import NodeList


class CMNode(ABC):
    """Base object in the model. An abstract class, handling the treelike
    structure"""

    def __init__(
            self,
            identifier: Optional[str] = None,  # Unique node id
    ) -> None:
        self.__id = identifier
        self.__children: NodeList = NodeList()

    @property
    def id(self) -> Optional[str]:
        """Get the id of the node"""
        return self.__id

    @property
    @abstractmethod
    def children(self) -> NodeList:
        """Get the children of this node. It's an abstract method since some
        components (widgets) may not have children, or the order of the
        children could be changed."""
        return self.__children
