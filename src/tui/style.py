"""
A style is a collection of sub-styles that describe the look and behaviour of a
component. Each sub-style contains multiple attribute-value pairs and is
related to a specific functionality. Sub-styles can be found in ./styles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, ClassVar
from tui._parser import Parser

from tui.styles.area import AreaInfo
from tui.styles.colour import ColourInfo
from tui.styles.compositor import CompositorInfo
from tui.styles.text import TextInfo


@dataclass
class Style:
    """Responsible for providing a collection of sub-styles and a globally
    compatible interface for interacting with them - setting and fetching their
    attributes. All components should have an instance of this class."""
    area_info: AreaInfo = field(default_factory=AreaInfo)
    compositor_info: CompositorInfo = field(default_factory=CompositorInfo)
    text_info: TextInfo = field(default_factory=TextInfo)
    colour_info: ColourInfo = field(default_factory=ColourInfo)

    # Contains a mapping of all the substyle attributes and the substyle they
    # are defined within in the following format:
    # attribute_name : sub_style
    _attribute_map: ClassVar[dict[str, str]]

    def get_value(self, attribute_name: str) -> Any:
        """Get a value, given its attribute name"""
        if attribute_name not in self._attribute_map:
            raise ValueError(f"Attribute '{attribute_name}' doesn't exist")

        style_type = getattr(self, self._attribute_map[attribute_name])
        return getattr(style_type, attribute_name)

    def set_value(self, attribute_name: str, value: Any) -> None:
        """Set the value of a style attribute"""
        if attribute_name not in self._attribute_map:
            raise ValueError(f"Attribute '{attribute_name}' doesn't exist")

        style_type = getattr(self, self._attribute_map[attribute_name])
        setattr(style_type, attribute_name, value)

    @staticmethod
    def _generate_attribute_map() -> dict[str, str]:
        """Create an attribute map for all the sub-styles. It contains a
        mapping of substyle attributes to the substyle they are declared in"""
        attribute_map = {}

        # Iterate over all the annotated names in this class. Due to it being
        # a dataclass, annotations are always used.
        # It's equivalent to iterating over all the substyles
        for style_name in Style.__annotations__.keys():
            # Ignore protected and private names
            if style_name.startswith('_'):
                continue

            # Iterate over the attributes of each substyle
            # A dummy class instance is required
            for attr in getattr(Style(), style_name).__annotations__.keys():
                # Ignore private names
                if "__" in attr:
                    continue

                # Since @property names are ignored in the aforementioned
                # iteration, styles with @property must define a protected
                # variable with the name of the property (starts with one
                # leading underscore)
                if attr.startswith('_'):
                    # Get the protected names and trim the underscore to match
                    # the property names (since we want to use @property and
                    # @property.setter)
                    attr = attr[1:]

                attribute_map[attr] = style_name

        return attribute_map

    @staticmethod
    def fromstr(string: str) -> Style:
        """Generate a style from a string that defines the deviations from the
        default style values. The string should be formatted in the following
        syntax: 'attribute=value, ...'
        See 'Parser.valid_str_to_style_pattern' for more details"""
        if not re.fullmatch(Parser.valid_str_to_style_pattern, string):
            raise ValueError("Invalid string format")

        # get all attribute-value pairs
        _attributes = re.findall(Parser.style_str_to_attr_and_val, string)
        # create a dictionary for O(1) search speed
        attributes = {pair[0]: pair[1] for pair in _attributes}
        attributes.pop('')  # An empty key is generated and has to be removed

        new_style = Style()

        # Return the default style if no attributes are specified
        if len(attributes) == 0:
            return new_style

        for attr, val in attributes.items():
            # If attribute name exists, get the style it's in and change its
            # value
            if attr in new_style._attribute_map:
                style_type = getattr(new_style, new_style._attribute_map[attr])
                match getattr(style_type, attr):  # get the expected value type
                    case bool():
                        if val == "True":
                            setattr(style_type, attr, True)
                        elif val == "False":
                            setattr(style_type, attr, False)
                        else:
                            raise ValueError(
                                    f"Invalid value {val} for attribute {attr}"
                                )
                    case int():
                        setattr(style_type, attr, int(val))
                    case str():
                        setattr(style_type, attr, val)
                    case _:  # custom types are assumed to work with strings
                        setattr(style_type, attr, val)
            else:
                raise ValueError(f"Attribute '{attr}' doesn't exist")

        return new_style


# _attribute_map must receive its value outside of class (post init)
Style._attribute_map = Style._generate_attribute_map()
