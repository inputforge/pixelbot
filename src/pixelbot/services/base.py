from abc import ABC
from abc import abstractmethod


class Service(ABC):
    def __init__(self):
        self._stop_requested = False

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    def start(self):
        self._stop_requested = False
        self.run()

    def stop(self):
        self._stop_requested = True
