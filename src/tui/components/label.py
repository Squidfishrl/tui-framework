"""A widget that can hold text which can be modified at runtime"""

from typing import Optional

from tui.components.widget import Widget
from tui.style import Style
from tui.styles.text import TextAlignment, VerticalAlignment


class Label(Widget):
    """ A widget that contains text
    Text position can be modified
    The text's contents can be changed at runtime
    """
    def __init__(
            self,
            identifier: Optional[str] = None,  # Unique identifier
            style: str | Style = Style(),  # Style properties for the component
            label_text: str = ""  # The text that's displayed on the label
    ) -> None:
        super().__init__(identifier=identifier, style=style)
        self.text = label_text

    def _render_to_area(self) -> None:
        """Render the label's text to its area"""
        self.area.area_ptr.reset_coords()
        self.area.add_chars(self.text)

    @property
    def text(self) -> str:
        """Get the label's text"""
        return self.__text

    @text.setter
    def text(self, new_text: str) -> None:
        """Set the label's text"""
        max_width = self.area.model.with_padding.columns
        max_height = self.area.model.with_padding.rows
        lines = []

        # apply text alignment to every line
        for line in new_text.split('\n'):
            if len(line) > max_width:
                raise ValueError("Text line is too long, cannot fit")

            match self.style.get_value("text_align"):
                case TextAlignment.LEFT:
                    lines.append(line)
                case TextAlignment.CENTER:
                    lines.append(line.center(max_width))
                case TextAlignment.RIGHT:
                    lines.append(f"{line:>{max_width}}")

            if len(lines) > max_height:
                raise ValueError("Too many lines, cannot fit")

        # apply vertical alignment
        remaining_lines = max_height - len(lines)
        match self.style.get_value("vertical_align"):
            case VerticalAlignment.TOP:
                self.__text = '\n'.join(lines)
            case VerticalAlignment.CENTER:
                self.__text = '\n' * int(remaining_lines/2) + '\n'.join(lines)
            case VerticalAlignment.BOTTOM:
                self.__text = '\n' * remaining_lines + '\n'.join(lines)

        self._render_to_area()

    @property
    def children(self) -> None:
        """Widgets can't have child components"""
        return super().children
