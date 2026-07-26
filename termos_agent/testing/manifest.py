from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import json


@dataclass
class TestStep:
    command: List[str]
    expect_exit_code: int = 0
    expect_files: List[str] = field(default_factory=list)


@dataclass
class TestCase:
    name: str
    description: str
    steps: List[TestStep] = field(default_factory=list)
    environment: Dict[str, Any] = field(default_factory=dict)


class TestManifestLoader:
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load(self) -> Dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as handle:
            if self.path.suffix.lower() == ".json":
                return json.load(handle)
            raise ValueError("Only JSON test manifests are supported for now.")
