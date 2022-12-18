"""Internal listing of children components used by the parent component"""

from _collections_abc import Sequence

from tui.component import Component


class NodeList(Sequence):
    """Internal listing of children components as a structure for the parent
    component
    """
    # insert_after/before index can be added

    def __init__(self) -> None:
        self._nodes_list: list[Component] = []  # preserve order
        # components with no id aren't in the dict
        self._nodes_dict: dict[str, Component] = {}  # fast search by index

    def __len__(self) -> int:
        return len(self._nodes_list)

    def __getitem__(self, index: int) -> Component:
        return self._nodes_list[index]

    def __setitem__(self, index: int, new_component: Component) -> None:
        prev_component = self._nodes_list[index]
        self._nodes_list[index] = new_component

        if prev_component.get_id() is not None:
            self._nodes_dict.pop(prev_component.get_id())
        if new_component.get_id() is not None:
            self._nodes_dict[new_component.get_id()] = new_component

    def __contains__(self, component: Component) -> bool:
        return component in self._nodes_list

    def get_component_with_id(self, identifier: str) -> Component | None:
        """Get component (search by id)"""
        return self._nodes_dict.get(identifier)

    def append(self, component: Component) -> None:
        """Add component at the end of the list"""
        if not isinstance(component, Component):
            raise TypeError

        if component in self._nodes_list:
            raise ValueError("Component exists already")

        if component.get_id() in self._nodes_dict:
            raise KeyError

        self._nodes_list.append(component)

        if component.get_id() is not None:
            self._nodes_dict[component.get_id()] = component

    def pop(self, index: int) -> Component:
        """Remove component (search by id)"""
        component = self._nodes_list.pop(index)

        if component.get_id() is not None:
            self._nodes_dict.pop(component.get_id())

        return component

    def remove(self, component: Component) -> None:
        """Remove component"""
        self._nodes_list.remove(component)
        if component.get_id() is not None:
            self._nodes_dict.pop(component.get_id())
