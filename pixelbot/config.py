import json
from typing import Any


def load_config() -> dict[str, Any]:
    with open('config.json') as f:
        return json.load(f)
