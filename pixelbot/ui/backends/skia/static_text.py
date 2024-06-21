import logging
from functools import cached_property

from skia import Canvas
from skia import Font
from skia import Paint
from skia import Rect
from skia import Size
from skia import TextEncoding

from pixelbot.ui.backends.skia.drawable import Drawable

log = logging.getLogger(__name__)


class StaticText(Drawable):
    def __init__(self, text: str, font: Font):
        super().__init__()
        self.text = text
        self.font = font

    @cached_property
    def text_bounds(self):
        bounds = Rect(0, 0, 0, 0)
        width = self.font.measureText(
            self.text, bounds=bounds, encoding=TextEncoding.kUTF8
        )

        return bounds, width

    @property
    def min_size(self):
        _, width = self.text_bounds
        return Size(width, self.font.getSize())

    def _draw(self, canvas: Canvas):
        if self.bounds is None:
            return

        log.debug("Rendering text %s at %s", self.text, self.bounds)

        paint = Paint()
        paint.setAntiAlias(True)
        paint.setColor(0xFFFFFFFF)

        text_bounds, _ = self.text_bounds

        x = self.bounds.x()
        y = self.bounds.y() - text_bounds.y()

        # Text is rendered from baseline
        log.debug("Actually painting text at (%s,%s)", x, y)
        canvas.drawSimpleText(self.text, x, y, self.font, paint)
