from typing import Any
from typing import get_type_hints

from pixelbot.services.manager import ServiceManager
from pixelbot.utils import load_class
from pixelbot.widgets.base import Widget


def load_widget(config: dict[str, Any], manager: ServiceManager) -> Widget:
    widget_class = load_class(config['class'])
    widget_config = config.get('config', {})

    type_hints = get_type_hints(widget_class.__init__)

    kwargs = {}

    for key, value in type_hints.items():
        if key == 'config':
            continue

        kwargs[key] = manager.get(value)

    if 'config' in type_hints:
        kwargs['config'] = widget_config

    return widget_class(**kwargs)
