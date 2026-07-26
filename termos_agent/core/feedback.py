from dataclasses import dataclass, field
import json
from typing import Any, Dict, List


@dataclass
class RunFeedback:
    kind: str
    name: str
    status: str
    environment: Dict[str, Any]
    command: List[str]
    stdout: str
    stderr: str
    exit_code: int
    runtime_seconds: float
    artifacts: List[str] = field(default_factory=list)
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "name": self.name,
            "status": self.status,
            "environment": self.environment,
            "command": self.command,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "runtime_seconds": self.runtime_seconds,
            "artifacts": self.artifacts,
            "notes": self.notes,
            "metadata": self.metadata,
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False)
