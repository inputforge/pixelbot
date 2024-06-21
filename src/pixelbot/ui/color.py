from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int
    alpha: int = 255

    def __int__(self):
        return self.alpha << 24 | self.red << 24 | self.green << 16 | self.blue << 8


def rgb(red: int, green: int, blue: int) -> Color:
    return Color(red, green, blue)


def rgba(red: int, green: int, blue: int, alpha: int) -> Color:
    return Color(red, green, blue, alpha)
