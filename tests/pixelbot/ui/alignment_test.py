from pixelbot.ui.alignment import align_center
from pixelbot.ui.alignment import align_start


def test_align_start():
    widths = [10, 20, 30]
    spacing = 5

    result = align_start(widths, spacing)

    assert result == [(0, 10), (15, 35), (40, 70)]


def test_align_center_single_child():
    axis_size = 100
    widths = [10]
    spacing = 5

    result = align_center(axis_size, widths, spacing)
    assert result == [(45, 55)]


def test_align_center_two_children():
    axis_size = 100
    widths = [10, 20]
    spacing = 10

    result = align_center(axis_size, widths, spacing)
    assert result == [(35, 45), (55, 75)]
