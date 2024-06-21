from skia import Rect
from skia import Size

from pixelbot.ui.backends.skia.box import Box


class VBox(Box):
    debug = True

    @property
    def min_size(self):
        width = 0
        height = 0

        for child in self.children:
            size = child.min_size
            width = max(width, size.width())
            height += size.height()
        return Size(width, height + self.spacing * (len(self.children) - 1))

    def _layout_align_start(self, bounds: Rect):
        x = bounds.left()
        y = bounds.top()
        for child in self.children:
            size = child.min_size
            child.layout(Rect(x, y, x + size.width(), y + size.height()))
            y += size.height() + self.spacing

    def _layout_align_center(self, bounds: Rect):
        y = bounds.top() + (bounds.height() - self.min_size.height()) / 2
        for child in self.children:
            size = child.min_size
            x = bounds.left() + (bounds.width() - size.width()) / 2
            child.layout(Rect(x, y, x + size.width(), y + size.height()))
            y += size.height() + self.spacing

    def _layout_align_end(self, bounds: Rect):
        size = self.min_size
        x = bounds.right() - size.width()
        y = bounds.bottom() - size.height()
        for child in self.children:
            child_size = child.min_size
            child.layout(Rect(x, y, x + child_size.width(), y + child_size.height()))
            y += child_size.height() + self.spacing

    def _layout_align_stretch(self, bounds: Rect):
        n = len(self.children)
        delta_y = bounds.height() / n - self.spacing

        x = bounds.left()
        y = bounds.top()

        for child in self.children:
            child_size = child.min_size
            child.layout(Rect(x, y, x + child_size.width(), y + delta_y))
            y += delta_y + self.spacing

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
