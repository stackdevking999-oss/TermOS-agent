from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TestFeedback:
    test_name: str
    status: str
    environment: Dict[str, Any]
    command: List[str]
    stdout: str
    stderr: str
    exit_code: int
    runtime_seconds: float
    artifacts: List[str] = field(default_factory=list)
    notes: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "test_name": self.test_name,
            "status": self.status,
            "environment": self.environment,
            "command": self.command,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "runtime_seconds": self.runtime_seconds,
            "artifacts": self.artifacts,
            "notes": self.notes,
        }
