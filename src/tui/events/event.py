"""Event class"""

from __future__ import annotations
from enum import Enum 
from typing import FrozenSet


class Modifiers(str, Enum):
    """Enumeration holding all modifiers we can listen to"""
    CONTROL = "ctrl"
    SHIFT = "shift"
    ALT = "alt"

    @staticmethod
    def contains(item: str) -> bool:
        try:
            Modifiers(item)
        except ValueError:
            return False
        else:
            return True


class Event:
    """Event class"""
    def __init__(self, modifiers: FrozenSet[Modifiers]):
        # convert string mod to enum
        self.modifiers: FrozenSet[Modifiers] = modifiers
