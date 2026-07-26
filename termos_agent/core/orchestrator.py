from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import json

from termos_agent.core.executor import Executor
from termos_agent.core.feedback import RunFeedback
from termos_agent.core.memory import MemoryStore
from termos_agent.core.planner import Planner
from termos_agent.core.repair import RepairEngine, RepairResult
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
        self.repair_engine = RepairEngine()
        self.memory.init_schema()

    def handle(self, request: str) -> OrchestrationResult:
        if request == "health-check":
            profile = self.inventory.as_dict()
            self.state.environment = profile
            feedback = RunFeedback(
                kind="environment",
                name="health-check",
                status="passed",
                environment=profile,
                command=[],
                stdout=json.dumps(profile),
                stderr="",
                exit_code=0,
                runtime_seconds=0.0,
                notes="Environment profile collected.",
            )
            self.memory.record_feedback(feedback)
            self.memory.record_environment(str(profile))
            self.memory.record_task(request, True, "Environment profile collected.")
            return OrchestrationResult(
                success=True,
                message="TermOS agent is alive.",
                data={"feedback": feedback.as_dict(), "environment": profile},
            )

        plan = self.planner.plan(request)
        feedback = RunFeedback(
            kind="task",
            name=request,
            status="planned" if plan.skill_name != "unknown" else "needs-action",
            environment=self.state.environment,
            command=[],
            stdout="",
            stderr="",
            exit_code=0,
            runtime_seconds=0.0,
            notes=f"Planner returned {plan.skill_name}: {plan.reason}",
            metadata={
                "skill": plan.skill_name,
                "reason": plan.reason,
                "steps": [step.__dict__ for step in plan.steps],
            },
        )
        self.memory.record_feedback(feedback)
        self.memory.record_task(request, False, f"Planner returned {plan.skill_name}.")
        return OrchestrationResult(
            success=False,
            message=f"Planner selected {plan.skill_name}: {plan.reason}",
            data={
                "feedback": feedback.as_dict(),
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
        run_feedback = result.feedback.to_run_feedback()
        self.memory.record_feedback(run_feedback)
        self.memory.record_test_run(
            result.feedback.test_name,
            result.feedback.status,
            str(result.feedback.as_dict()),
        )
        return OrchestrationResult(
            success=result.passed,
            message=f"Test {result.feedback.test_name} finished with status {result.feedback.status}.",
            data={"feedback": result.feedback.as_dict(), "run_feedback": run_feedback.as_dict()},
        )

    def diagnose_failure(self, feedback: RunFeedback) -> OrchestrationResult:
        repair: RepairResult = self.repair_engine.analyze(feedback)
        self.memory.record_repair(repair.feedback, repair.should_retry)
        return OrchestrationResult(
            success=repair.should_retry,
            message=f"Repair classified {repair.feedback.metadata.get('category', 'unknown')}.",
            data={
                "feedback": repair.feedback.as_dict(),
                "suggestions": [suggestion.__dict__ for suggestion in repair.suggestions],
                "should_retry": repair.should_retry,
                "auto_apply": repair.auto_apply,
            },
        )
