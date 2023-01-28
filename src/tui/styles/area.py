"""Describe area parameters"""

from dataclasses import dataclass


@dataclass
class AreaInfo:
    """Define properties for a component's area:
        size
        margin offset
        padding offset
    """
    rows: int = 0
    columns: int = 0

    margin_top: int = 0
    margin_bottom: int = 0
    margin_left: int = 0
    margin_right: int = 0

    padding_top: int = 0
    padding_bottom: int = 0
    padding_left: int = 0
    padding_right: int = 0
