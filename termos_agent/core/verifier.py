from pathlib import Path

from termos_agent.core.executor import CommandResult


class Verifier:
    def file_exists(self, path: str) -> bool:
        return Path(path).exists()

    def command_succeeded(self, result: CommandResult) -> bool:
        return result.returncode == 0

    def non_empty_output(self, text: str) -> bool:
        return bool(text.strip())
