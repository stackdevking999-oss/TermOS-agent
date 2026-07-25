from dataclasses import asdict, dataclass
import platform
import shutil
from typing import Dict


@dataclass
class EnvironmentProfile:
    system: str
    machine: str
    python: str
    tools: Dict[str, str]


class Inventory:
    def build_profile(self) -> EnvironmentProfile:
        tools = {name: shutil.which(name) or "" for name in ["git", "python", "curl", "wget", "java", "node"]}
        return EnvironmentProfile(
            system=platform.system(),
            machine=platform.machine(),
            python=platform.python_version(),
            tools=tools,
        )

    def as_dict(self) -> dict:
        return asdict(self.build_profile())
