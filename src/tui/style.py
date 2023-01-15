"""Used to craete style for components"""

from dataclasses import dataclass, field
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
class CompositorInfo:
    """Define properties that define how the component is composed"""
    # is the component inserted on the current row, or on the next one
    inline: bool = False


@dataclass
class Style:
    """Collection of proprties that can define the look of a component"""
    area_info: AreaInfo = field(default_factory=AreaInfo)
    compositor_info: CompositorInfo = field(default_factory=CompositorInfo)
    colour_info: ColourInfo = field(default_factory=ColourInfo)
