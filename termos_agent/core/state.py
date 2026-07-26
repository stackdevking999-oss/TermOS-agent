from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class RuntimeState:
    environment: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, Any] = field(default_factory=dict)
    active_task: str = ""
    mode: str = "dev"
