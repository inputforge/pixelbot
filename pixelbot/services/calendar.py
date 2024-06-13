import logging
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import timedelta
from time import sleep
from typing import Any
from typing import Iterator

import requests
from icalendar import Calendar

from pixelbot.services.base import Service

log = logging.getLogger(__name__)


@dataclass
class Event:
    title: str
    start: datetime
    calendar_name: str


def _normalize_datetime(dt: datetime | date) -> datetime:
    current_tz = datetime.now().astimezone().tzinfo
    if isinstance(dt, datetime):
        return dt

    return datetime.combine(dt, datetime.min.time(), tzinfo=current_tz)


def next_event_from_url(ical_url: str) -> Iterator[Event]:
    response = requests.get(ical_url)

    if response.status_code != 200:
        log.error(
            "Failed to fetch calendar data from %s due to %s %s",
            ical_url,
            response.status_code,
            response.text,
        )
        return iter([])

    cal = Calendar.from_ical(response.content)

    events = []
    for component in cal.walk(name="VEVENT"):
        events.append(
            Event(
                title=str(component.get("summary")),
                start=_normalize_datetime(component.get("dtstart").dt),
                calendar_name=str(cal["X-WR-CALNAME"])
                if "X-WR-CALNAME" in cal
                else "Unnamed Calendar",
            )
        )

    # Filter future events and sort them by start time
    now = datetime.now().astimezone()
    return (event for event in events if now < event.start < now + timedelta(days=1))


class CalendarService(Service):
    def __init__(self, config: dict[str, Any]):
        super().__init__()
        self.calendars = config["calendars"]
        self.__next_events = []

    @property
    def next_event(self):
        return next(
            (e for e in self.__next_events if e.start > datetime.now().astimezone()),
            None,
        )

    def update(self):
        log.info("Updating calendar data")
        # Update the calendar data from  the configured iCal feeds
        self.__next_events = sorted(
            (
                event
                for calendar in self.calendars
                for event in next_event_from_url(calendar["url"])
            ),
            key=lambda event: event.start,
        )

    def run(self):
        while not self._stop_requested:
            self.update()
            sleep(300)
