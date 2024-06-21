from collections.abc import Sequence
from typing import Literal

from skia import Canvas
from skia import Rect
from skia import Size

from pixelbot.ui.alignment import Alignment
from pixelbot.ui.alignment import align
from pixelbot.ui.alignment import justify
from pixelbot.ui.backends.skia.drawable import Drawable


class Box(Drawable):
    def __init__(
        self,
        axis: Literal["horizontal", "vertical"],
        children: Sequence[Drawable],
        spacing: int = 8,
        align: Alignment = "start",
        justify: Alignment = "start",
    ):
        super().__init__()
        self.children = children
        self.axis = axis
        self.align = align
        self.justify = justify
        self.spacing = spacing

    def _draw(self, canvas: Canvas):
        for child in self.children:
            child.render(canvas)

    @property
    def min_size(self):
        total_spacing = self.spacing * (len(self.children) - 1)

        width = total_spacing if self.axis == "horizontal" else 0
        height = total_spacing if self.axis == "vertical" else 0

        for child in self.children:
            size = child.min_size

            if self.axis == "horizontal":
                height = max(height, size.height())
                width += size.width()
            else:
                width = max(width, size.width())
                height += size.height()

        return Size(width, height)

    def layout(self, bounds: Rect):
        super().layout(bounds)

        widths = [child.min_size.width() for child in self.children]
        heights = [child.min_size.height() for child in self.children]

        if self.axis == "horizontal":
            child_x = align(self.align, bounds.width(), self.spacing, widths)
            child_y = justify(self.justify, bounds.height(), heights)
        else:
            child_x = justify(self.justify, bounds.width(), widths)
            child_y = align(self.align, bounds.height(), self.spacing, heights)

        for child, x_bounds, y_bounds in zip(self.children, child_x, child_y):
            x, x_ = x_bounds
            y, y_ = y_bounds
            rect = Rect(x, y, x_, y_)
            rect.offset(bounds.x(), bounds.y())
            child.layout(rect)
