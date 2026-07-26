from dataclasses import dataclass
import json
import time
from typing import Any, Dict, List

from termos_agent.core.executor import Executor
from termos_agent.core.verifier import Verifier
from termos_agent.environment.inventory import Inventory
from termos_agent.testing.feedback import TestFeedback


@dataclass
class TestResult:
    feedback: TestFeedback
    passed: bool


class TestingRunner:
    def __init__(self) -> None:
        self.executor = Executor()
        self.verifier = Verifier()
        self.inventory = Inventory()

    def run_manifest(self, manifest: Dict[str, Any]) -> TestResult:
        start = time.time()
        environment = manifest.get("environment") or self.inventory.as_dict()
        test_name = manifest.get("name", "unnamed")
        steps = manifest.get("steps", [])
        artifacts: List[str] = []
        stdout_chunks: List[str] = []
        stderr_chunks: List[str] = []
        status = "passed"
        exit_code = 0
        command: List[str] = []

        for step in steps:
            command = list(step.get("command", []))
            if not command:
                status = "failed"
                stderr_chunks.append("Empty command in test step.")
                exit_code = 1
                break

            result = self.executor.run(command, timeout=int(step.get("timeout_seconds", 60)))
            stdout_chunks.append(result.stdout)
            stderr_chunks.append(result.stderr)
            exit_code = result.returncode

            if result.returncode != int(step.get("expect_exit_code", 0)):
                status = "failed"
                break

            for expected in step.get("expect_files", []):
                if not self.verifier.file_exists(expected):
                    status = "failed"
                    stderr_chunks.append(f"Missing expected file: {expected}")
                    exit_code = 1
                    break
                artifacts.append(expected)
            if status == "failed":
                break

        runtime = time.time() - start
        feedback = TestFeedback(
            test_name=test_name,
            status=status,
            environment=environment,
            command=command,
            stdout="\n".join(chunk for chunk in stdout_chunks if chunk).strip(),
            stderr="\n".join(chunk for chunk in stderr_chunks if chunk).strip(),
            exit_code=exit_code,
            runtime_seconds=runtime,
            artifacts=artifacts,
            notes=json.dumps({"step_count": len(steps)}),
        )
        return TestResult(feedback=feedback, passed=status == "passed")
