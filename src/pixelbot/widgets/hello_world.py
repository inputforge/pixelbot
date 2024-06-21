from pixelbot.ui.color import rgb
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
                ),
                Text(
                    text="I'm a Pixelbot!",
                    font=Fonts.PIXELIFY_SANS.size(75),
                ),
                align="center",
                justify="center",
            ),
            border=25,
            background=rgb(0, 0, 0),
            foreground=rgb(255, 255, 255),
        )
