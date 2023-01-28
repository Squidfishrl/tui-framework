"""Describe area parameters"""

from dataclasses import dataclass


@dataclass
class AreaInfo:
    """Define properties for a component's area"""
    rows: int = 0
    columns: int = 0
