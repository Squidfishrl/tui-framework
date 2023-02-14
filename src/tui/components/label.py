"""A widget that can hold text which can be modified at runtime"""

from typing import Optional

from tui.components.widget import Widget
from tui.style import Style
from tui.styles.text import TextAlignment


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
        self.text = label_text
        super().__init__(identifier=identifier, style=style)

    def _render_to_area(self) -> None:
        """Render the label's text to its area"""
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

        for line in new_text.split('\n'):
            if len(line) > max_width:
                raise ValueError("Text line is too long, cannot fit")

            match self.style.get_value("text_align"):
                case TextAlignment.CENTER:
                    lines.append(line.center(max_width))
                case TextAlignment.LEFT:
                    lines.append(line)
                case TextAlignment.RIGHT:
                    lines.append(f"{line:>{max_width}}")

            if len(lines) > max_height:
                raise ValueError("Too many text lines, cannot fit")

        self.__text = '\n'.join(lines)

    @property
    def children(self) -> None:
        """Widgets can't have child components"""
        return super().children
