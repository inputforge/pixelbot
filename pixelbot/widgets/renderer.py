from collections.abc import Callable
from typing import Any

from wx import ALIGN_CENTER
from wx import ALIGN_LEFT
from wx import ALIGN_RIGHT
from wx import ALL
from wx import BITMAP_TYPE_ANY
from wx import EXPAND
from wx import HORIZONTAL
from wx import VERTICAL
from wx import Bitmap
from wx import BoxSizer
from wx import Font
from wx import FontInfo
from wx import Frame
from wx import Panel
from wx import Sizer
from wx import StaticBitmap
from wx import StaticText
from wx import WrapSizer
from wx.lib.ticker import Ticker

from pixelbot.widgets.base import Widget
from pixelbot.widgets.controls import Alignment
from pixelbot.widgets.controls import Container
from pixelbot.widgets.controls import Control
from pixelbot.widgets.controls import If
from pixelbot.widgets.controls import Image
from pixelbot.widgets.controls import Screen
from pixelbot.widgets.controls import ScrollText
from pixelbot.widgets.controls import Text
from pixelbot.widgets.controls import VBox


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
                flag=self._get_flags(control),
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
        else:
            raise NotImplementedError(f"Control {control} is not supported")

    def render(self, frame: Frame, widget: Widget):
        screen = widget.create_screen()
        self._render_screen(screen, frame)

    def _render_text(self, control: Text, panel):
        is_dynamic = callable(control.text)

        text = StaticText(panel, label=control.text() if is_dynamic else control.text)
        text.SetFont(Font(FontInfo(control.font.size).FaceName(control.font.name)))

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
        flag = 0

        if control.border:
            flag |= ALL

        if control.align == Alignment.STRETCH:
            flag |= EXPAND
        elif control.align == Alignment.CENTER:
            flag |= ALIGN_CENTER
        elif control.align == Alignment.START:
            flag |= ALIGN_LEFT
        elif control.align == Alignment.END:
            flag |= ALIGN_RIGHT

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
