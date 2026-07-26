from dataclasses import dataclass
from typing import Any, Dict, Optional

from termos_agent.environment.capabilities import CapabilityRegistry
from termos_agent.skills.registry import SkillRegistry


@dataclass
class PlannedStep:
    action: str
    target: str
    args: Dict[str, Any]


@dataclass
class Plan:
    skill_name: str
    steps: list[PlannedStep]
    reason: str


class Planner:
    def __init__(self, capabilities: Optional[CapabilityRegistry] = None, skills: Optional[SkillRegistry] = None) -> None:
        self.capabilities = capabilities or CapabilityRegistry()
        self.skills = skills or SkillRegistry()

    def plan(self, request: str) -> Plan:
        request_lower = request.lower()

        if "health" in request_lower:
            return Plan(skill_name="health-check", steps=[PlannedStep("probe", "environment", {})], reason="health request")

        if "apk" in request_lower and ("decode" in request_lower or "decompile" in request_lower):
            return Plan(skill_name="decode_apk", steps=[PlannedStep("run", "apktool", {"command": ["apktool", "d"]})], reason="apk decode request")

        if "apk" in request_lower and ("build" in request_lower or "compile" in request_lower):
            return Plan(skill_name="build_apk", steps=[PlannedStep("run", "apktool", {"command": ["apktool", "b"]})], reason="apk build request")

        if "apk" in request_lower and ("sign" in request_lower or "signature" in request_lower):
            return Plan(skill_name="sign_apk", steps=[PlannedStep("run", "apksigner", {"command": ["apksigner"]})], reason="apk sign request")

        return Plan(skill_name="unknown", steps=[], reason="no rule matched")
