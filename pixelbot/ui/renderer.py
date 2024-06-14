from collections.abc import Callable
from typing import Any

from wx import ALIGN_BOTTOM
from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_CENTER_VERTICAL
from wx import ALIGN_LEFT
from wx import ALIGN_RIGHT
from wx import ALIGN_TOP
from wx import ALL
from wx import BITMAP_TYPE_ANY
from wx import EXPAND
from wx import HORIZONTAL
from wx import VERTICAL
from wx import Bitmap
from wx import BoxSizer
from wx import Colour
from wx import Font
from wx import FontInfo
from wx import Frame
from wx import Panel
from wx import Size
from wx import Sizer
from wx import StaticBitmap
from wx import StaticText
from wx import WrapSizer
from wx.lib.ticker import Ticker

from pixelbot.ui.color import Color
from pixelbot.ui.color import rgb
from pixelbot.ui.controls import Alignment
from pixelbot.ui.controls import Container
from pixelbot.ui.controls import Control
from pixelbot.ui.controls import If
from pixelbot.ui.controls import Image
from pixelbot.ui.controls import Screen
from pixelbot.ui.controls import ScrollText
from pixelbot.ui.controls import Spacer
from pixelbot.ui.controls import Text
from pixelbot.ui.controls import VBox
from pixelbot.widgets.base import Widget


def _color(c: Color):
    return Colour(c.red, c.green, c.blue, c.alpha)


class Renderer:
    def __init__(self):
        self.dynamic_controls: list[Callable | tuple[Any, str, Callable[[], Any]]] = []

    def _render_container(self, control: Container, panel: Panel) -> Sizer:
        sizer = BoxSizer(VERTICAL if isinstance(control, VBox) else HORIZONTAL)

        for child in control.children:
            value = self._render_control(child, panel)
            sizer.Add(
                value,
                proportion=child.bias,
                flag=self._get_flags(child),
                border=control.border,
            )

        return sizer

    def _render_control(self, control: Control, panel: Panel):
        if isinstance(control, Container):
            return self._render_container(control, panel)
        elif isinstance(control, Text):
            return self._render_text(control, panel)
        elif isinstance(control, ScrollText):
            return self._render_scroll_text(control, panel)
        elif isinstance(control, Image):
            return self._render_image(control, panel)
        elif isinstance(control, If):
            return self._render_if(control, panel)
        elif isinstance(control, Spacer):
            return self._render_spacer(control, panel)
        else:
            raise NotImplementedError(f"Control {control} is not supported")

    def render(self, frame: Frame, widget: Widget):
        screen = widget.create_screen()
        self._render_screen(screen, frame)

    def _render_text(self, control: Text, panel):
        is_dynamic = callable(control.text)

        text = StaticText(panel, label=control.text() if is_dynamic else control.text)
        text.SetFont(
            Font(
                FontInfo(Size(control.font.size, control.font.size)).FaceName(
                    control.font.name
                )
            )
        )

        if control.wrap:
            text.Wrap(control.wrap)

        if is_dynamic:
            self.dynamic_controls.append((text, "SetLabel", control.text))

        return text

    def update(self):
        for item in self.dynamic_controls:
            if callable(item):
                item()
            else:
                control, attr, func = item
                getattr(control, attr)(func())

    def _render_screen(self, screen: Screen, frame: Frame):
        panel = Panel(frame)
        sizer = WrapSizer()
        sizer.Add(
            self._render_control(screen.root, panel), flag=ALL, border=screen.border
        )
        panel.SetSizer(sizer)
        panel.SetBackgroundColour(_color(screen.background))
        panel.SetForegroundColour(_color(screen.foreground))

    def _render_image(self, control: Image, panel: Panel):
        bitmap = Bitmap(control.src, BITMAP_TYPE_ANY)
        return StaticBitmap(panel, bitmap=bitmap)

    def _render_scroll_text(self, control, panel):
        is_dynamic = callable(control.text)

        ticker = Ticker(
            text=control.text() if is_dynamic else control.text,
            parent=panel,
            ppf=control.ppf,
            fps=control.fps,
        )
        ticker.SetFont(Font(FontInfo(control.font.size).FaceName(control.font.name)))

        if is_dynamic:
            self.dynamic_controls.append((ticker, "SetText", control.text))

        return ticker

    def _get_flags(self, control: Control) -> int:
        flag = ALL

        # if control.border:
        #     flag |= ALL

        if control.horizontal_alignment == Alignment.STRETCH:
            flag |= EXPAND
        elif control.horizontal_alignment == Alignment.CENTER:
            flag |= ALIGN_CENTER_HORIZONTAL
        elif control.horizontal_alignment == Alignment.START:
            flag |= ALIGN_LEFT
        elif control.horizontal_alignment == Alignment.END:
            flag |= ALIGN_RIGHT

        if control.vertical_alignment == Alignment.STRETCH:
            flag |= EXPAND
        elif control.vertical_alignment == Alignment.CENTER:
            flag |= ALIGN_CENTER_VERTICAL
        elif control.vertical_alignment == Alignment.START:
            flag |= ALIGN_TOP
        elif control.vertical_alignment == Alignment.END:
            flag |= ALIGN_BOTTOM

        return flag

    def _render_if(self, control: If, panel):
        sizer = WrapSizer()

        then = self._render_control(control.then, panel)
        else_ = self._render_control(control.else_, panel)

        sizer.Add(then)
        sizer.Add(else_)

        def _update():
            if control.condition():
                sizer.Show(then, True, recursive=True)
                sizer.Show(else_, False, recursive=True)
            else:
                sizer.Show(then, False, recursive=True)
                sizer.Show(else_, True, recursive=True)

            sizer.Layout()
            panel.Layout()

        self.dynamic_controls.append(_update)
        _update()
        return sizer

    def _render_spacer(self, control: Spacer, panel):
        if control.invisible:
            return Size(0, 0)

        text = StaticText(panel, label=" ")
        text.SetBackgroundColour(_color(rgb(255, 0, 0)))
        text.SetForegroundColour(_color(rgb(0, 0, 255)))
        return text
