from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol

from termos_agent.core.workflow_registry import WorkflowDefinition, WorkflowRegistry, WorkflowStepSpec


@dataclass
class ReasoningDecision:
    request: str
    workflow_name: str = ""
    skill_name: str = ""
    reason: str = ""
    confidence: float = 0.0
    steps: List[Dict[str, Any]] = field(default_factory=list)
    needs_llm: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReasoningAdapter(Protocol):
    def analyze(self, request: str, environment: Dict[str, Any] | None = None) -> ReasoningDecision: ...


class LocalReasoningAdapter:
    """Rule-based reasoning seam used until an LLM is attached."""

    def __init__(self, workflows: WorkflowRegistry | None = None) -> None:
        self.workflows = workflows or WorkflowRegistry()

    def analyze(self, request: str, environment: Dict[str, Any] | None = None) -> ReasoningDecision:
        matched = self.workflows.match_request(request)
        if matched:
            return self._from_workflow(request, matched, environment or {})

        return ReasoningDecision(
            request=request,
            reason="No known workflow matched; needs reasoning model input.",
            confidence=0.2,
            needs_llm=True,
            metadata={"matched_workflow": None, "environment": environment or {}},
        )

    def _from_workflow(
        self,
        request: str,
        workflow: WorkflowDefinition,
        environment: Dict[str, Any],
    ) -> ReasoningDecision:
        return ReasoningDecision(
            request=request,
            workflow_name=workflow.name,
            skill_name=workflow.skill_name,
            reason=f"Matched workflow {workflow.name}.",
            confidence=0.92,
            steps=[self._step_to_dict(step) for step in workflow.steps],
            needs_llm=False,
            metadata={
                "description": workflow.description,
                "keywords": list(workflow.keywords),
                "environment": environment,
            },
        )

    @staticmethod
    def _step_to_dict(step: WorkflowStepSpec) -> Dict[str, Any]:
        return {"action": step.action, "target": step.target, "args": step.args}
