from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int
    alpha: int = 255


def rgb(red: int, green: int, blue: int) -> Color:
    return Color(red, green, blue)


def rgba(red: int, green: int, blue: int, alpha: int) -> Color:
    return Color(red, green, blue, alpha)
