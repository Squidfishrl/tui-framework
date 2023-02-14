"""Used to create style for components"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, ClassVar

from tui.styles.area import AreaInfo
from tui.styles.colour import ColourInfo
from tui.styles.compositor import CompositorInfo
from tui.styles.text import TextInfo


@dataclass
class Style:
    """Collection of properties that can define the look of a component"""
    area_info: AreaInfo = field(default_factory=AreaInfo)
    compositor_info: CompositorInfo = field(default_factory=CompositorInfo)
    colour_info: ColourInfo = field(default_factory=ColourInfo)
    text_info: TextInfo = field(default_factory=TextInfo)

    # validate that string format is correct and can be converted to a style
    __validate_str_pattern: ClassVar[re.Pattern] = re.compile(r"""
[ \n]* # non strict newlines and whitespaces
(?:\w+) # attribute name
[ \n]*
=
[ \n]*
(?:\w+|\d+) # attribute value (string or whole number)
(?: # group for multiple attribute-value pairs
[ \n]*
, # separator for attribute-value pairs
[ \n]*
(?:\w+)
[ \n]*
=
[ \n]*
(?:\w+|\d+)
)* # can have any amount of attribute-value pairs
[ \n]*
,? # can end with or without a comma
[ \n]*
""", re.VERBOSE)
    # get attribute and value to convert to style
    __str_pattern_to_attr_and_val: ClassVar[re.Pattern] = re.compile(r"""
(?: # group attribute-value pairs
(\w+) # get attribute name
[ \n]* # non strict newlines and whitespaces
=
[ \n]*
(\w+|\d+) # get attribute value (string or integer)
)* # repeat group for every pair
""", re.VERBOSE)

    # attribute_name: style_type pair
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
        """Create an attribute map for all the styles"""
        attribute_map = {}

        # iterate over style types
        for style_name in Style.__annotations__.keys():
            if style_name.startswith('_'):
                continue

            # iterate over attributes of individual styles
            # dummy class instance is required
            for attr in getattr(Style(), style_name).__annotations__.keys():
                if "__" in attr:
                    continue

                # Since @property is ignored, styles with @property must
                # define a variable with the name of the property and
                # a leading udnerscore
                if attr.startswith('_'):
                    # trim the underscore to match the property name
                    attr = attr[1:]

                attribute_map[attr] = style_name

        print(attribute_map)
        return attribute_map

    @staticmethod
    def fromstr(string: str) -> Style:
        """Create a style from a string"""
        if not re.fullmatch(Style.__validate_str_pattern, string):
            raise ValueError("Invalid string format")

        _attributes = re.findall(Style.__str_pattern_to_attr_and_val, string)
        attributes = {pair[0]: pair[1] for pair in _attributes}
        attributes.pop('')  # empty key is generated and has to be removed

        new_style = Style()

        # Return default style if no attributes are specified
        if len(attributes) == 0:
            return new_style

        for attr, val in attributes.items():
            # if attribute name exists get the style it's in and
            # change it's value
            if attr in new_style._attribute_map:
                style_type = getattr(new_style, new_style._attribute_map[attr])
                match getattr(style_type, attr):
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
            else:
                raise ValueError(f"Attribute '{attr}' doesn't exist")

        return new_style


# _attribute_map must receive value outside of class
Style._attribute_map = Style._generate_attribute_map()
