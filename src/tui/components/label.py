"""
A label is a widget that holds text and is capable of aligning the text within
itself. Dynamic changes to the label's text should are also handled
"""

from typing import Optional
import re

from tui.components.widget import Widget
from tui._parser import Parser
from tui.style import Style
from tui.styles.text import TextAlignment, VerticalAlignment


class Label(Widget):
    """ A widget that contains text
    Text position can be modified
    The text's contents can be changed at runtime
    """
    def __init__(
            self,
            label_text: str = "",  # The text that's displayed on the label
            style: str | Style = Style(),  # Style properties for the component
            identifier: Optional[str] = None,  # Unique identifier
    ) -> None:
        super().__init__(identifier=identifier, style=style)
        self.text = label_text

    def _render_to_area(self) -> None:
        """Render the label's text to its area"""
        self.area.area_ptr.reset_coords()
        self.area.add_chars(self.text)

    def clear(self) -> None:
        """Clear existing area"""
        self.text = (self.area.model.with_padding.columns *
                     self.area.model.with_padding.rows *
                     " ")

    @property
    def text(self) -> str:
        """Get the label's text"""
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        """Set the label's text"""
        max_width = self.area.model.with_padding.columns
        max_height = self.area.model.with_padding.rows
        lines = []

        cannot_wrap = not self.style.get_value("text_wrap")

        # apply text alignment to every line
        for line in new_text.split('\n'):
            if len(line) > max_width * max_height:
                raise ValueError("Text line is too long, cannot fit")

            if cannot_wrap and len(line) > max_width:
                raise ValueError("Text line is too long, cannot fit")

            wrapped_lines = re.findall(Parser.auto_wrap_text(max_width), line)
            for _line in wrapped_lines[:-1]:  # last value is a dud so trim it
                # align text horizontally
                match self.style.get_value("text_align"):
                    case TextAlignment.LEFT:
                        lines.append(_line)
                    case TextAlignment.CENTER:
                        lines.append(_line.center(max_width))
                    case TextAlignment.RIGHT:
                        lines.append(f"{_line:>{max_width}}")

                if len(lines) > max_height:
                    raise ValueError("Too many lines, cannot fit")

        # apply vertical alignment
        remaining_lines = max_height - len(lines)
        match self.style.get_value("vertical_align"):
            case VerticalAlignment.TOP:
                self._text = '\n'.join(lines)
            case VerticalAlignment.CENTER:
                self._text = '\n' * int(remaining_lines/2) + '\n'.join(lines)
            case VerticalAlignment.BOTTOM:
                self._text = '\n' * remaining_lines + '\n'.join(lines)

        self._render_to_area()

    @property
    def children(self) -> None:
        """Widgets can't have child components"""
        return super().children
