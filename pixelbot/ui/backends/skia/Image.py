from functools import cached_property

from skia import Canvas
from skia import Image as SkiaImage
from skia import Size

from pixelbot.ui.backends.skia.drawable import Drawable


class Image(Drawable):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    @cached_property
    def _skia_image(self):
        return SkiaImage.open(self.path)

    @property
    def min_size(self):
        bounds = self._skia_image.bounds()
        return Size(bounds.width(), bounds.height())

    def _draw(self, canvas: Canvas):
        canvas.drawImageRect(self._skia_image, self._skia_image.bounds(), self.bounds)
