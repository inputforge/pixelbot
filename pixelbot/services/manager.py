from threading import Thread
from typing import Any
from typing import TypeVar

from pixelbot.services.base import Service
from pixelbot.utils import load_class

T = TypeVar("T", bound=Service)


class ServiceManager:
    def __init__(self) -> None:
        self._services = []
        self._started = False
        self._threads = []

    def load(self, config: list[dict[str, Any]]) -> None:
        for service in config:
            service_class = load_class(service["class"])
            service_config = service.get("config", {})
            self.register(service_class(service_config))

    def get(self, service_class: type[T]) -> T:
        for service in self._services:
            if isinstance(service, service_class):
                return service

        raise ValueError(f"Service {service_class} not found")

    def register(self, service: Service) -> None:
        self._services.append(service)

    def start(self) -> None:
        if self._started:
            return

        for service in self._services:
            thread = Thread(target=service.start)
            thread.start()
            self._threads.append(thread)

        self._started = True

    def stop(self) -> None:
        for service in self._services:
            service.stop()

        for thread in self._threads:
            thread.join()

        self._started = False
