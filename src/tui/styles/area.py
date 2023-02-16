"""This substyle describes the area box-model, as well as the component's
size."""

from dataclasses import dataclass


@dataclass
class AreaInfo:
    """Defines properties for a component's area:
        size
        margin offset
        padding offset
    """
    rows: int = 1
    columns: int = 1

    margin_top: int = 0
    margin_bottom: int = 0
    margin_left: int = 0
    margin_right: int = 0
    # tell Style that there's a margin property
    _margin: int = 0

    padding_top: int = 0
    padding_bottom: int = 0
    padding_left: int = 0
    padding_right: int = 0
    # tell Style that there's a padding property
    _padding: int = 0

    @property
    def margin(self) -> tuple[int, int, int, int] | int:
        """Get all margins"""
        margins = (self.margin_top, self.margin_bottom, self.margin_left,
                   self.margin_right)
        if margins[0] == margins[1] == margins[2] == margins[3]:
            return self.margin_top

        return margins

    @margin.setter
    def margin(self, margins: tuple[int, int, int, int] | int) -> None:
        """Set all margins"""
        if isinstance(margins, tuple):
            self.margin_top = margins[0]
            self.margin_bottom = margins[1]
            self.margin_left = margins[2]
            self.margin_right = margins[3]
        else:
            self.margin_top = margins
            self.margin_bottom = margins
            self.margin_left = margins
            self.margin_right = margins

    @property
    def padding(self) -> tuple[int, int, int, int] | int:
        """Get all paddings"""
        paddings = (self.padding_top, self.padding_bottom, self.padding_left,
                    self.padding_right)

        if paddings[0] == paddings[1] == paddings[2] == paddings[3]:
            return self.padding_top

        return paddings

    @padding.setter
    def padding(self, paddings: tuple[int, int, int, int] | int) -> None:
        """Set all paddings"""
        if isinstance(paddings, tuple):
            self.padding_top = paddings[0]
            self.padding_bottom = paddings[1]
            self.padding_left = paddings[2]
            self.padding_right = paddings[3]
        else:
            self.padding_top = paddings
            self.padding_bottom = paddings
            self.padding_left = paddings
            self.padding_right = paddings
