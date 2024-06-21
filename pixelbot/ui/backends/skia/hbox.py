from skia import Rect
from skia import Size

from pixelbot.ui.backends.skia.box import Box


class HBox(Box):
    @property
    def min_size(self):
        width = 0
        height = 0

        for child in self.children:
            size = child.min_size
            height = max(height, size.height())
            width += size.width()
        return Size(width + self.spacing * (len(self.children) - 1), height)

    def _layout_align_start(self, bounds: Rect):
        x = bounds.left()
        y = bounds.top()
        for child in self.children:
            size = child.min_size
            child.layout(Rect(x, y, x + size.width(), y + size.height()))
            x += size.width() + self.spacing

    def _layout_align_center(self, bounds: Rect):
        x = bounds.left() + (bounds.width() - self.min_size.width()) / 2
        for child in self.children:
            size = child.min_size
            y = bounds.top() + (bounds.height() - size.height()) / 2
            child.layout(Rect(x, y, x + size.width(), y + size.height()))
            x += size.width() + self.spacing

    def _layout_align_end(self, bounds: Rect):
        x = bounds.right() - self.min_size.width()
        y = bounds.bottom() - self.min_size.height()
        for child in self.children:
            size = child.min_size
            child.layout(Rect(x, y, x + size.width(), y + size.height()))
            x += size.width() + self.spacing

    def _layout_align_stretch(self, bounds: Rect):
        n = len(self.children)
        delta_x = bounds.width() / n - self.spacing

        x = bounds.left()
        y = bounds.top()

        for child in self.children:
            child_size = child.min_size
            child.layout(Rect(x, y, x + delta_x, y + child_size.height()))
            x += delta_x + self.spacing

    def layout(self, bounds: Rect):
        super().layout(bounds)
        if self.align == "start":
            self._layout_align_start(bounds)
        elif self.align == "center":
            self._layout_align_center(bounds)
        elif self.align == "end":
            self._layout_align_end(bounds)
        elif self.align == "stretch":
            self._layout_align_stretch(bounds)
