from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Capability:
    name: str
    preferred_tools: List[str]
    fallback_tools: List[str]


class CapabilityRegistry:
    def __init__(self) -> None:
        self._capabilities: Dict[str, Capability] = {
            "search_files": Capability("search_files", ["rg"], ["grep"]),
            "download_file": Capability("download_file", ["curl"], ["wget", "python"]),
            "run_shell": Capability("run_shell", ["bash"], ["sh"]),
            "decode_apk": Capability("decode_apk", ["apktool"], []),
            "build_apk": Capability("build_apk", ["apktool"], []),
            "sign_apk": Capability("sign_apk", ["apksigner"], []),
        }

    def get(self, name: str) -> Capability | None:
        return self._capabilities.get(name)
