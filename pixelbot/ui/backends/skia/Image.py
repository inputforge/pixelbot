from functools import cached_property

from skia import Canvas
from skia import Image as SkiaImage
from skia import Size

from pixelbot.ui.backends.skia.context import current_context
from pixelbot.ui.backends.skia.drawable import Drawable


def choose_image(path: dict[int, str]) -> str:
    context = current_context()
    dppx = context.dppx

    iterator = iter(sorted(path.items()))
    best_match = next(iterator)[1]

    for scale, image_path in iterator:
        if scale <= dppx:
            best_match = image_path
        else:
            break

    return best_match


class Image(Drawable):
    def __init__(self, path: str | dict[int, str]):
        super().__init__()
        self.path = path if isinstance(path, str) else choose_image(path)

    @cached_property
    def _skia_image(self):
        return SkiaImage.open(self.path)

    @property
    def min_size(self):
        bounds = self._skia_image.bounds()
        return Size(bounds.width(), bounds.height())

    def _draw(self, canvas: Canvas):
        canvas.drawImageRect(self._skia_image, self._skia_image.bounds(), self.bounds)
