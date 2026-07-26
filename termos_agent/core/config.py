from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class AppConfig:
    data: Dict[str, Any]


class ConfigLoader:
    def __init__(self, path: str = "config/default.yaml") -> None:
        self.path = Path(path)

    def load(self) -> AppConfig:
        if not self.path.exists():
            return AppConfig(data={})
        with self.path.open("r", encoding="utf-8") as handle:
            return AppConfig(data=yaml.safe_load(handle) or {})
