from datetime import datetime
from zoneinfo import ZoneInfo

from babel import default_locale
from babel import Locale
from babel.dates import format_date
from babel.dates import format_time
from babel.dates import format_timedelta

from pixelbot.services.calendar import CalendarService
from pixelbot.widgets.base import Widget
from pixelbot.widgets.controls import HBox
from pixelbot.widgets.controls import If
from pixelbot.widgets.controls import Image
from pixelbot.widgets.controls import Screen
from pixelbot.widgets.controls import Text
from pixelbot.widgets.controls import VBox
from pixelbot.widgets.fonts import Fonts


class CalendarWidget(Widget):

    def __init__(self, calendar_service: CalendarService):
        self.calendar_service = calendar_service
        current_locale = default_locale('LC_TIME') or 'en'
        self.locale = Locale.parse(current_locale)

    @property
    def update_interval(self) -> int:
        return 1000

    def __get_current_time(self):
        return format_time(datetime.now(), 'h:mm a', locale=self.locale)

    def __get_current_date(self):
        return format_date(datetime.now(), 'MMMd', locale=self.locale)

    def __has_next_event(self):
        return self.calendar_service.next_event is not None

    def __get_next_event_name(self):
        if not self.__has_next_event():
            return ''

        return self.calendar_service.next_event.title

    def __get_next_event_date(self):
        if not self.__has_next_event():
            return ''

        delta = self.calendar_service.next_event.start - datetime.now(tz=ZoneInfo('UTC'))
        return f"in {format_timedelta(delta, granularity='minute', locale=self.locale)}"

    def create_screen(self) -> Screen:
        return Screen(
            VBox(
                HBox(
                    Image('calendar.png', bias=0),
                    VBox(
                        Text(self.__get_current_time, font=Fonts.SILKSREEN.size(72)),
                        Text(self.__get_current_date, font=Fonts.SILKSREEN.size(56))
                    )
                ),
                If(self.__has_next_event,
                   VBox(
                       Text('Next event', font=Fonts.SILKSREEN.size(48)),
                       Text(self.__get_next_event_name, font=Fonts.SILKSREEN.size(72)),
                       Text(self.__get_next_event_date, font=Fonts.SILKSREEN.size(56))
                   ),
                   Text('Your day is clear!', font=Fonts.SILKSREEN.size(64))
                   ),
            ),
            border=25
        )
