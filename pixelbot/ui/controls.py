from collections.abc import Callable
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pixelbot.ui.color import Color
from pixelbot.ui.color import rgb
from pixelbot.ui.color import rgba
from pixelbot.ui.fonts import Font
from pixelbot.ui.fonts import Fonts


class Alignment(Enum):
    START = "start"
    CENTER = "center"
    END = "end"
    STRETCH = "stretch"


@dataclass(frozen=True, kw_only=True)
class Control:
    border: int = 0
    horizontal_alignment: Alignment = Alignment.START
    vertical_alignment: Alignment = Alignment.START
    bias: int = 1


class Container(Control):
    children: Iterable[Control]

    def __init__(self, *children: Control, **kwargs: Any):
        super().__init__(**kwargs)
        self.children = children


@dataclass(frozen=True)
class Screen:
    root: Container
    border: int = 0
    background: Color = rgb(255, 255, 255)
    foreground: Color = rgb(0, 0, 0)


class VBox(Container):
    pass


class HBox(Container):
    pass


@dataclass(frozen=True)
class Spacer(Control):
    invisible: bool = True


@dataclass(frozen=True)
class Text(Control):
    text: str | Callable[[], str]
    font: Font = Fonts.SILKSREEN
    wrap: int | None = None


@dataclass(frozen=True)
class ScrollText(Control):
    text: str | Callable[[], str]
    font: Font = Fonts.SILKSREEN
    fps: int = 24
    ppf: int = 30
    foreground: Color = rgb(0, 0, 0)
    background: Color = rgba(0, 0, 0, 0)


@dataclass(frozen=True)
class Image(Control):
    src: str


@dataclass(frozen=True)
class If(Control):
    condition: Callable[[], bool]
    then: Control
    else_: Control | None = None
