"""The base event class which all event types inherit from."""

from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import FrozenSet


class Modifiers(str, Enum):
    """Enumeration responsible for holding all modifiers we can listen to"""
    CONTROL = "ctrl"
    SHIFT = "shift"
    ALT = "alt"

    @staticmethod
    def contains(item: str) -> bool:
        """Does a string exist as a Modifier value?"""
        try:
            Modifiers(item)
        except ValueError:
            return False
        else:
            return True


class Event(ABC):
    """Base event class. All event classes should inherit from it."""
    def __init__(self, modifiers: FrozenSet[Modifiers]):
        self.modifiers: FrozenSet[Modifiers] = modifiers
