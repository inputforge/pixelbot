from collections.abc import Sequence
from typing import Literal

from skia import Canvas

from pixelbot.ui.backends.skia.drawable import Drawable


class Box(Drawable):
    def __init__(
        self,
        children: Sequence[Drawable],
        spacing: int = 8,
        align: Literal["start", "center", "end", "stretch"] = "start",
    ):
        super().__init__()
        self.children = children
        self.align = align
        self.spacing = spacing

    def _draw(self, canvas: Canvas):
        for child in self.children:
            child.render(canvas)
