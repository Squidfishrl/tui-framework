"""Used to craete style for components"""

from dataclasses import dataclass
from enum import Enum, auto
import colorama as Colour


class MeasurementUnit(Enum):
    """Possible measurement units for the style properties describing length"""
    PERCENT = auto()
    CHAR = auto()


@dataclass
class AreaInfo:
    """Define properties for area expansion"""
    # the unit `rows` are measured in
    rows_mu: MeasurementUnit = MeasurementUnit.CHAR
    min_rows: int = 0  # the rows a component can't shrink below
    max_rows: int = 0  # the rows a component can't grow beyond

    # the unit `columns` are measured in
    columns_mu: MeasurementUnit = MeasurementUnit.CHAR
    min_columns: int = 0  # the columns a component can't shrink below
    max_columns: int = 0  # the columns a component can't grow beyond


@dataclass
class ColourInfo:
    """Define properties for component colouring"""
    foreground: Colour.Fore = Colour.Fore.WHITE  # default foreground colour
    background: Colour.Back = Colour.Back.BLACK  # default background colour


@dataclass
class Style:
    """Collection of proprties that can define the look of a component"""

    area_info: AreaInfo = AreaInfo()  # properties for area expansion
    colour_info: ColourInfo = ColourInfo  # properties for component colouring
