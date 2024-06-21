import logging

from skia import Canvas
from skia import Font
from skia import Rect
from skia import Typeface

from pixelbot.ui import controls
from pixelbot.ui.backends.skia.box import Box
from pixelbot.ui.backends.skia.context import Context
from pixelbot.ui.backends.skia.context import ctx
from pixelbot.ui.backends.skia.Image import Image
from pixelbot.ui.backends.skia.spacer import Spacer
from pixelbot.ui.backends.skia.static_text import StaticText
from pixelbot.widgets.base import Widget

log = logging.getLogger(__name__)


def _choose_image(ctx: Context, path: dict[int, str]) -> str:
    match = path[1]
    scale = round(ctx.dppx)

    for i in range(1, scale + 1):
        match = path.get(i, match)

    return match


class SkiaRenderer:
    def __init__(self, ctx: Context):
        self.context = ctx

    def render(self, canvas: Canvas, widget: Widget, bounds: Rect):
        with ctx(self.context):
            screen = widget.create_screen()

            control = self._render_screen(screen)
            border = screen.border * self.context.dppx
            screen_bounds = Rect(
                border,
                border,
                bounds.width() - border,
                bounds.height() - border,
            )
            control.layout(screen_bounds)
            control.render(canvas)

    def _render_screen(self, screen: controls.Screen):
        return self._render_control(screen.root)

    def _render_control(self, control: controls.Control):
        if isinstance(control, controls.HBox):
            children = [self._render_control(child) for child in control.children]
            return Box(
                "horizontal", children, align=control.align, justify=control.justify
            )
        elif isinstance(control, controls.VBox):
            children = [self._render_control(child) for child in control.children]
            return Box(
                "vertical", children, align=control.align, justify=control.justify
            )
        elif isinstance(control, controls.Text):
            text = control.text() if callable(control.text) else control.text
            typeface = Typeface(control.font.name)
            size = control.font.size * self.context.dppx
            return StaticText(text, Font(typeface, size=size))
        elif isinstance(control, controls.Spacer):
            return Spacer()
        elif isinstance(control, controls.Image):
            return Image(
                control.src
                if isinstance(control.src, str)
                else _choose_image(self.context, control.src)
            )
        elif isinstance(control, controls.If):
            return (
                self._render_control(control.then)
                if control.condition()
                else self._render_control(control.else_)
            )
        else:
            raise ValueError(f"Unsupported control type {type(control)}")
