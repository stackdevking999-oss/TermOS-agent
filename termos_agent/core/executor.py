from dataclasses import dataclass
import subprocess
from typing import Sequence


@dataclass
class CommandResult:
    command: Sequence[str]
    returncode: int
    stdout: str
    stderr: str


class Executor:
    def run(self, command: Sequence[str], timeout: int = 60, cwd: str | None = None) -> CommandResult:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return CommandResult(
            command=command,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
