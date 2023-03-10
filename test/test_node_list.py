"""Test that src/_node_list.py works correctly"""
import pytest

from tui._node_list import NodeList
from tui.components.division import Division


@pytest.fixture
def empty_list():
    """Return an empty node list"""
    return NodeList()


@pytest.fixture
def one_component():
    """Return one component"""
    return Division(identifier="one component")


@pytest.fixture
def ten_components():
    """Return ten components"""
    return [Division(identifier=str(i)) for i in range(10)]


@pytest.fixture
def ten_component_list():
    """Return a list with ten components"""
    _list = NodeList()
    for component in [Division(identifier=str(i)) for i in range(10)]:
        _list.append(component)

    return _list


def test_empty_list(empty_list):
    """Test that NodeList has 0 components before being mutated"""
    assert len(empty_list) == 0


def test_append_one_component(empty_list: NodeList, one_component: Division):
    """Test that NodeList updates its length when one component is added"""
    empty_list.append(one_component)
    assert len(empty_list) == 1


def test_append_existing_component(
        empty_list: NodeList,
        one_component: Division
        ):
    """Test that duplicate components cannot be added"""
    with pytest.raises(ValueError):
        empty_list.append(one_component)
        empty_list.append(one_component)


def test_append_many(empty_list: NodeList, ten_components: list[Division]):
    """Test that NodeList updates its length when many components are added"""
    for component in ten_components:
        empty_list.append(component)

    assert len(empty_list) == 10


def test_get_item(ten_component_list: NodeList):
    """Test that components in NodeList can be accessed with []"""
    for i in range(10):
        if not isinstance(ten_component_list[i], Division):
            assert False

    assert True


def test_get_item_with_invalid_index(
        ten_component_list: NodeList,
        one_component: Division
):
    """Test that using an index out of scope raises an IndexError"""
    with pytest.raises(IndexError):
        ten_component_list[50] = one_component  # test accessing


def test_set_item(ten_component_list: NodeList, one_component: Division):
    """Test that an existing component in NodeList can be reset"""
    ten_component_list[0] = one_component
    assert ten_component_list[0].id == one_component.id


def test_does_not_contain_component(
        ten_component_list: NodeList,
        one_component: Division
        ):
    """Test that a component doesn't exist in NodeList"""
    assert one_component not in ten_component_list


def test_contains_component(
        ten_component_list: NodeList,
        one_component: Division
        ):
    """Test that a component exists in NodeList"""
    ten_component_list[4] = one_component
    assert one_component in ten_component_list


def test_get_component_with_id(ten_component_list: NodeList):
    """Test that a component with the corresponding id is returned"""
    assert isinstance(ten_component_list.get_by_id("4"), Division)


def test_get_component_with_invalid_id(ten_component_list: NodeList):
    """Test that a component with the corresponding id is returned"""
    assert ten_component_list.get_by_id("Y") is None


def test_pop_component(ten_component_list: NodeList):
    """Test that the component with the corresponding index is removed"""
    removed_component = ten_component_list.pop(2)
    assert removed_component not in ten_component_list


def test_remove_component(ten_component_list: NodeList):
    """Test that the correspondig component is removed and NodeList length is
    correct"""
    component = ten_component_list[5]
    ten_component_list.remove(component)
    assert len(ten_component_list) == 9


def test_internal_dict_is_updated(ten_component_list: NodeList):
    """Test that after all functions the internal dictionary is correctly being
    updated"""
    for _ in range(6):
        ten_component_list.pop(0)  # 6 7 8 9

    ten_component_list.remove(ten_component_list[1])  # 6 8 9 at this point

    ten_component_list.append(Division(identifier="l"))

    assert list(ten_component_list._nodes_dict.keys()) == ["6", "8", "9", "l"]
