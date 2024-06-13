from importlib import import_module
from typing import Any


def load_class(name: str) -> Any:
    module_name, class_name = name.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, class_name)
