from abc import ABC
from abc import abstractmethod
from random import randint
from typing import ClassVar

from skia import Canvas
from skia import Paint
from skia import Rect

from pixelbot.ui.backends.skia.context import current_context


class Drawable(ABC):
    debug: ClassVar[bool] = False

    def __init__(self, width: int = 0, height: int = 0):
        self.bounds: Rect = Rect(0, 0, width, height)

    @property
    @abstractmethod
    def min_size(self):
        raise NotImplementedError

    @property
    def max_size(self):
        return self.min_size

    def layout(self, bounds: Rect):
        self.bounds = bounds

    @abstractmethod
    def _draw(self, canvas: Canvas):
        raise NotImplementedError

    def render(self, canvas: Canvas):
        context = current_context()
        if context.debug or self.debug:
            paint = Paint()
            paint.setStyle(Paint.kFill_Style)
            paint.setARGB(255, randint(0, 255), randint(0, 255), randint(0, 255))
            canvas.drawRect(self.bounds, paint)

        self._draw(canvas)
