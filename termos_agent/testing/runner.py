from dataclasses import dataclass
from typing import Any, Dict

from termos_agent.testing.feedback import TestFeedback


@dataclass
class TestResult:
    feedback: TestFeedback
    passed: bool


class TestingRunner:
    def run_manifest(self, manifest: Dict[str, Any]) -> TestResult:
        feedback = TestFeedback(
            test_name=manifest.get("name", "unnamed"),
            status="skipped",
            environment=manifest.get("environment", {}),
            command=[],
            stdout="",
            stderr="Testing runner not implemented yet.",
            exit_code=0,
            runtime_seconds=0.0,
        )
        return TestResult(feedback=feedback, passed=False)
