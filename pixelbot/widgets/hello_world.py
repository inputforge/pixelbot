from pixelbot.ui.color import rgb
from pixelbot.ui.controls import Alignment
from pixelbot.ui.controls import Screen
from pixelbot.ui.controls import Text
from pixelbot.ui.controls import VBox
from pixelbot.ui.fonts import Fonts
from pixelbot.widgets.base import Widget


class HelloWorldWidget(Widget):
    def create_screen(self):
        return Screen(
            root=VBox(
                Text(
                    text="Hello, World!",
                    font=Fonts.PIXELIFY_SANS.size(100),
                    horizontal_alignment=Alignment.CENTER,
                    vertical_alignment=Alignment.CENTER,
                ),
                Text(
                    text="I'm a happy little Pixelbot!",
                    font=Fonts.PIXELIFY_SANS.size(75),
                    horizontal_alignment=Alignment.CENTER,
                    vertical_alignment=Alignment.CENTER,
                ),
                align=Alignment.CENTER,
                justify=Alignment.CENTER,
            ),
            border=25,
            background=rgb(0, 0, 0),
            foreground=rgb(255, 255, 255),
        )
