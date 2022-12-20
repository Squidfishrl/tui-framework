"""Node definition creating a DOM-like structure"""

from abc import ABC, abstractmethod

import tui._node_list as nl


class CMNode(ABC):
    """Base object in the model"""

    def __init__(
            self,
            identifier: str | None = None,  # unique id for the node
            name: str | None = None  # for debug readability
    ) -> None:
        self.__id = identifier
        self.__name = name
        self.__children: nl.NodeList = nl.NodeList()

    @property
    def id(self) -> str | None:
        """Get the id of the node"""
        return self.__id

    @property
    def name(self) -> str | None:
        """Get the name of this node"""
        return self.__name

    @property
    @abstractmethod
    def children(self) -> nl.NodeList:
        """Return children of this node
            abstract method since some components may not have children"""
        return self.__children
