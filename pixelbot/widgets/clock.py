from datetime import datetime

from babel import Locale
from babel import default_locale
from babel.dates import format_date
from babel.dates import format_time

from pixelbot.ui.color import rgb
from pixelbot.ui.controls import Alignment
from pixelbot.ui.controls import Screen
from pixelbot.ui.controls import Text
from pixelbot.ui.controls import VBox
from pixelbot.ui.fonts import Fonts
from pixelbot.widgets.base import Widget


class ClockWidget(Widget):
    def __init__(self):
        current_locale = default_locale("LC_TIME") or "en"
        self.locale = Locale.parse(current_locale)

    @property
    def update_interval(self) -> int:
        return 1000

    def __get_current_time(self):
        return format_time(datetime.now(), "HH:mm", locale=self.locale)

    def __get_current_date(self):
        return format_date(datetime.now(), "short", locale=self.locale)

    def create_screen(self) -> Screen:
        return Screen(
            VBox(
                Text(
                    text=self.__get_current_time,
                    font=Fonts.SILKSREEN.size(325),
                    horizontal_alignment=Alignment.CENTER,
                    vertical_alignment=Alignment.CENTER,
                ),
                Text(
                    text=self.__get_current_date,
                    font=Fonts.SILKSREEN.size(100),
                    horizontal_alignment=Alignment.CENTER,
                    vertical_alignment=Alignment.CENTER,
                ),
                align=Alignment.CENTER,
            ),
            border=25,
            background=rgb(0, 0, 0),
            foreground=rgb(255, 255, 255),
        )
