"""All regex patterns can be found here. This is done, as to not pollute the
other classes with long regex patterns."""

from functools import cache
import re


class Parser:
    """Responsible for holding all regex patters"""

    # validate that string format is correct and can be converted to a style
    valid_str_to_style_pattern: re.Pattern
    # used for fetching attribute-value pairs from a style string
    style_str_to_attr_and_val: re.Pattern

    @staticmethod
    @cache
    def auto_wrap_text(max_width: int):
        """Used to split text into smaller parts"""
        return re.compile("(.{0," + str(max_width) + "})(?: | ?$)")


Parser.valid_str_to_style_pattern = re.compile(r"""
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

Parser.style_str_to_attr_and_val = re.compile(r"""
(?: # group attribute-value pairs
(\w+) # get attribute name
[ \n]* # non strict newlines and whitespaces
=
[ \n]*
(\w+|\d+) # get attribute value (string or integer)
)* # repeat group for every pair
""", re.VERBOSE)
