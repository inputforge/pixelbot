from skia import Canvas
from skia import Size

from pixelbot.ui.backends.skia.drawable import Drawable


class Spacer(Drawable):
    def __init__(self):
        super().__init__()

    @property
    def min_size(self):
        return Size(0, 0)

    def _draw(self, canvas: Canvas):
        pass
