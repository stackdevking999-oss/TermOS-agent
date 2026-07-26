from dataclasses import dataclass
from typing import Any, Dict

from termos_agent.core.executor import Executor
from termos_agent.core.memory import MemoryStore
from termos_agent.core.planner import Planner
from termos_agent.core.state import RuntimeState
from termos_agent.core.verifier import Verifier
from termos_agent.environment.inventory import Inventory
from termos_agent.skills.registry import SkillRegistry


@dataclass
class OrchestrationResult:
    success: bool
    message: str
    data: Dict[str, Any]


class Orchestrator:
    def __init__(self) -> None:
        self.state = RuntimeState()
        self.inventory = Inventory()
        self.executor = Executor()
        self.verifier = Verifier()
        self.memory = MemoryStore()
        self.skills = SkillRegistry()
        self.planner = Planner(skills=self.skills)
        self.memory.init_schema()

    def handle(self, request: str) -> OrchestrationResult:
        if request == "health-check":
            profile = self.inventory.as_dict()
            self.state.environment = profile
            self.memory.record_task(request, True, "Environment profile collected.")
            return OrchestrationResult(
                success=True,
                message="TermOS agent is alive.",
                data=profile,
            )

        plan = self.planner.plan(request)
        self.memory.record_task(request, False, f"Planner returned {plan.skill_name}.")
        return OrchestrationResult(
            success=False,
            message=f"Planner selected {plan.skill_name}: {plan.reason}",
            data={
                "request": request,
                "skill": plan.skill_name,
                "reason": plan.reason,
                "steps": [step.__dict__ for step in plan.steps],
            },
        )
