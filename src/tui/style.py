"""Used to create style for components"""

from dataclasses import dataclass, field

from tui.styles.area import AreaInfo
from tui.styles.colour import ColourInfo
from tui.styles.compositor import CompositorInfo


@dataclass
class Style:
    """Collection of properties that can define the look of a component"""
    area_info: AreaInfo = field(default_factory=AreaInfo)
    compositor_info: CompositorInfo = field(default_factory=CompositorInfo)
    colour_info: ColourInfo = field(default_factory=ColourInfo)
