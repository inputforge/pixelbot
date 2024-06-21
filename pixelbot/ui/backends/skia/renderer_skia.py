import logging

from skia import Canvas
from skia import Font
from skia import Rect
from skia import Typeface

from pixelbot.ui import controls
from pixelbot.ui.backends.skia.context import Context
from pixelbot.ui.backends.skia.context import context
from pixelbot.ui.backends.skia.hbox import HBox
from pixelbot.ui.backends.skia.Image import Image
from pixelbot.ui.backends.skia.spacer import Spacer
from pixelbot.ui.backends.skia.static_text import StaticText
from pixelbot.ui.backends.skia.vbox import VBox
from pixelbot.widgets.base import Widget

log = logging.getLogger(__name__)


class SkiaRenderer:
    def __init__(self, ctx: Context):
        self.context = ctx

    def render(self, canvas: Canvas, widget: Widget, bounds: Rect):
        with context(self.context):
            screen = widget.create_screen()

            control = self._render_screen(screen)
            screen_bounds = Rect(
                screen.border,
                screen.border,
                bounds.width() - screen.border,
                bounds.height() - screen.border,
            )
            control.layout(screen_bounds)
            control.render(canvas)

    def _render_screen(self, screen: controls.Screen):
        return self._render_control(screen.root)

    def _render_control(self, control: controls.Control):
        if isinstance(control, controls.HBox):
            children = [self._render_control(child) for child in control.children]
            return HBox(children, align=control.align)
        elif isinstance(control, controls.VBox):
            children = [self._render_control(child) for child in control.children]
            return VBox(children, align=control.align)
        elif isinstance(control, controls.Text):
            text = control.text() if callable(control.text) else control.text
            typeface = Typeface(control.font.name)
            return StaticText(text, Font(typeface, size=control.font.size))
        elif isinstance(control, controls.Spacer):
            return Spacer()
        elif isinstance(control, controls.Image):
            return Image(control.src)
        elif isinstance(control, controls.If):
            return (
                self._render_control(control.then)
                if control.condition()
                else self._render_control(control.else_)
            )
        else:
            raise ValueError(f"Unsupported control type {type(control)}")
