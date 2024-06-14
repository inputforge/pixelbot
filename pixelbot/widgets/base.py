from abc import ABC
from abc import abstractmethod

from pixelbot.ui.controls import Screen


class Widget(ABC):
    @abstractmethod
    def create_screen(self) -> Screen:
        raise NotImplementedError

    @property
    def update_interval(self) -> int:
        return 0
