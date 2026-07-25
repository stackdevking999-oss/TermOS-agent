from dataclasses import dataclass
from typing import Callable, Dict


@dataclass
class Skill:
    name: str
    description: str
    handler: Callable


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)
