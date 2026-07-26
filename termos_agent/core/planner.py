from dataclasses import dataclass
from typing import Any, Dict, Optional

from termos_agent.environment.capabilities import CapabilityRegistry
from termos_agent.core.reasoning import LocalReasoningAdapter, ReasoningDecision
from termos_agent.core.workflow_registry import WorkflowRegistry
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
    workflow_name: str = ""
    confidence: float = 0.0
    metadata: Dict[str, Any] | None = None


class Planner:
    def __init__(
        self,
        capabilities: Optional[CapabilityRegistry] = None,
        skills: Optional[SkillRegistry] = None,
        workflows: Optional[WorkflowRegistry] = None,
        reasoning: Optional[LocalReasoningAdapter] = None,
    ) -> None:
        self.capabilities = capabilities or CapabilityRegistry()
        self.skills = skills or SkillRegistry()
        self.workflows = workflows or WorkflowRegistry()
        self.reasoning = reasoning or LocalReasoningAdapter(self.workflows)

    def plan(self, request: str, environment: Dict[str, Any] | None = None) -> Plan:
        decision: ReasoningDecision = self.reasoning.analyze(request, environment or {})
        if not decision.needs_llm:
            return Plan(
                skill_name=decision.skill_name,
                steps=[PlannedStep(**step) for step in decision.steps],
                reason=decision.reason,
                workflow_name=decision.workflow_name,
                confidence=decision.confidence,
                metadata=decision.metadata,
            )

        request_lower = request.lower()

        if "health" in request_lower:
            return Plan(
                skill_name="health-check",
                steps=[PlannedStep("probe", "environment", {})],
                reason="health request",
                workflow_name="health_check",
                confidence=0.9,
                metadata={"source": "rule"},
            )

        if "apk" in request_lower and ("decode" in request_lower or "decompile" in request_lower):
            return Plan(
                skill_name="decode_apk",
                steps=[PlannedStep("run", "apktool", {"command": ["apktool", "d"]})],
                reason="apk decode request",
                workflow_name="decode_apk",
                confidence=0.85,
                metadata={"source": "rule"},
            )

        if "apk" in request_lower and ("build" in request_lower or "compile" in request_lower):
            return Plan(
                skill_name="build_apk",
                steps=[PlannedStep("run", "apktool", {"command": ["apktool", "b"]})],
                reason="apk build request",
                workflow_name="build_apk",
                confidence=0.85,
                metadata={"source": "rule"},
            )

        if "apk" in request_lower and ("sign" in request_lower or "signature" in request_lower):
            return Plan(
                skill_name="sign_apk",
                steps=[PlannedStep("run", "apksigner", {"command": ["apksigner"]})],
                reason="apk sign request",
                workflow_name="sign_apk",
                confidence=0.85,
                metadata={"source": "rule"},
            )

        return Plan(skill_name="unknown", steps=[], reason="no rule matched", metadata={"source": "rule"})
