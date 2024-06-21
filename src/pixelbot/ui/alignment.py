from typing import Literal

Alignment = Literal["start", "center", "end", "stretch"]


def align_start(children_sizes: list[int], spacing: int) -> list[tuple[int, int]]:
    x = 0
    result = []
    for size in children_sizes:
        result.append((x, x + size))
        x += size + spacing
    return result


def align_center(
    axis_size: int, children_sizes: list[int], spacing: int
) -> list[tuple[int, int]]:
    x = (axis_size - sum(children_sizes) - spacing * (len(children_sizes) - 1)) // 2
    result = []
    for size in children_sizes:
        result.append((x, x + size))
        x += size + spacing
    return result


def align_end(
    axis_size: int, children_sizes: list[int], spacing: int
) -> list[tuple[int, int]]:
    x = axis_size - sum(children_sizes) - spacing * (len(children_sizes) - 1)
    result = []
    for size in children_sizes:
        result.append((x, x + size))
        x += size + spacing
    return result


def align_stretch(
    axis_size: int, children_sizes: list[int], spacing: int
) -> list[tuple[int, int]]:
    n = len(children_sizes)
    delta = axis_size // n - spacing
    result = []
    x = 0
    for _ in children_sizes:
        result.append((x, x + delta))
        x += delta + spacing
    return result


def align(
    alignment: Alignment, axis_size: int, spacing: int, children_sizes: list[int]
) -> list[tuple[int, int]]:
    if alignment == "start":
        return align_start(children_sizes, spacing)
    if alignment == "center":
        return align_center(axis_size, children_sizes, spacing)
    if alignment == "end":
        return align_end(axis_size, children_sizes, spacing)
    if alignment == "stretch":
        return align_stretch(axis_size, children_sizes, spacing)

    raise ValueError(f"Invalid alignment {align}")


def justify_start(children_sizes):
    return [(0, size) for size in children_sizes]


def justify_end(axis_size, children_sizes):
    return [(axis_size - size, axis_size) for size in children_sizes]


def justify_center(axis_size, children_sizes):
    return [
        ((axis_size - size) // 2, (axis_size + size) // 2) for size in children_sizes
    ]


def justify_stretch(axis_size, children_sizes):
    return [(0, axis_size) for _ in children_sizes]


def justify(
    alignment: Alignment, axis_size: int, children_sizes: list[int]
) -> list[tuple[int, int]]:
    if alignment == "start":
        return justify_start(children_sizes)
    if alignment == "end":
        return justify_end(axis_size, children_sizes)
    if alignment == "center":
        return justify_center(axis_size, children_sizes)
    if alignment == "stretch":
        return justify_stretch(axis_size, children_sizes)

    raise ValueError(f"Invalid justify {alignment}")
