from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from termos_agent.core.executor import Executor
from termos_agent.core.memory import MemoryStore
from termos_agent.core.planner import Planner
from termos_agent.core.state import RuntimeState
from termos_agent.core.verifier import Verifier
from termos_agent.environment.inventory import Inventory
from termos_agent.skills.registry import SkillRegistry
from termos_agent.testing.manifest import TestManifestLoader
from termos_agent.testing.runner import TestingRunner


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
        self.tester = TestingRunner()
        self.memory.init_schema()

    def handle(self, request: str) -> OrchestrationResult:
        if request == "health-check":
            profile = self.inventory.as_dict()
            self.state.environment = profile
            self.memory.record_environment(str(profile))
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

    def run_test_manifest(self, manifest_path: str) -> OrchestrationResult:
        path = Path(manifest_path)
        manifest = TestManifestLoader(str(path)).load()
        result = self.tester.run_manifest(manifest)
        self.memory.record_test_run(
            result.feedback.test_name,
            result.feedback.status,
            str(result.feedback.as_dict()),
        )
        return OrchestrationResult(
            success=result.passed,
            message=f"Test {result.feedback.test_name} finished with status {result.feedback.status}.",
            data=result.feedback.as_dict(),
        )
