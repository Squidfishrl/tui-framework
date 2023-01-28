"""Describe how component composition should work"""

from dataclasses import dataclass


@dataclass
class CompositorInfo:
    """Define properties, describing component composition"""
    inline: bool = False  # are child components inserted on the same row
