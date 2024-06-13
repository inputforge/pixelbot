from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Callable
from typing import Iterable

from pixelbot.widgets.color import Color
from pixelbot.widgets.color import rgb
from pixelbot.widgets.color import rgba
from pixelbot.widgets.fonts import Font
from pixelbot.widgets.fonts import Fonts


class Alignment(Enum):
    START = 'start'
    CENTER = 'center'
    END = 'end'
    STRETCH = 'stretch'


@dataclass(frozen=True, kw_only=True)
class Control:
    border: int = 0
    align: Alignment = Alignment.START
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


class VBox(Container):
    pass


class HBox(Container):
    pass


@dataclass(frozen=True)
class Text(Control):
    text: str | Callable[[], str]
    font: Font = Fonts.SILKSREEN


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
