"""Describes how every part of a border should look."""

from abc import ABC


class Border(ABC):
    """Abstract class for describing borders"""
    vertical: str
    horizontal: str
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str


class DefaultBorder(Border):
    """Default border for components
    ╔═╗
    ║x║
    ╚═╝
    """
    vertical = '║'
    horizontal = '═'
    top_left = '╔'
    top_right = '╗'
    bottom_right = '╝'
    bottom_left = '╚'
