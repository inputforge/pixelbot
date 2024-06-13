from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Font:
    name: str
    size: int


class Fonts(Enum):
    SILKSREEN = Font("Silkscreen", 12)
    PRESS_START_2P = Font("Press Start 2P", 12)
    PIXELIFY_SANS = Font("Pixelify Sans", 12)
    TINY_5X3 = Font("Tiny5", 12)
    MICRO_5 = Font("Micro5", 12)

    def size(self, size: int) -> Font:
        return Font(self.value.name, size)
