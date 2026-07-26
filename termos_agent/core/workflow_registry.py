from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class WorkflowStepSpec:
    action: str
    target: str
    args: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkflowDefinition:
    name: str
    description: str
    skill_name: str
    keywords: Tuple[str, ...]
    steps: Tuple[WorkflowStepSpec, ...]


class WorkflowRegistry:
    def __init__(self) -> None:
        self._workflows: Dict[str, WorkflowDefinition] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register(
            WorkflowDefinition(
                name="health_check",
                description="Collect a system profile and verify core runtime state.",
                skill_name="health-check",
                keywords=("health", "status", "check", "system"),
                steps=(WorkflowStepSpec("probe", "environment", {}),),
            )
        )
        self.register(
            WorkflowDefinition(
                name="decode_apk",
                description="Decode an APK project with apktool.",
                skill_name="decode_apk",
                keywords=("decode", "decompile", "apk"),
                steps=(WorkflowStepSpec("run", "apktool", {"command": ["apktool", "d"]}),),
            )
        )
        self.register(
            WorkflowDefinition(
                name="build_apk",
                description="Build an APK project with apktool.",
                skill_name="build_apk",
                keywords=("build", "compile", "apk"),
                steps=(WorkflowStepSpec("run", "apktool", {"command": ["apktool", "b"]}),),
            )
        )
        self.register(
            WorkflowDefinition(
                name="sign_apk",
                description="Sign an APK with apksigner.",
                skill_name="sign_apk",
                keywords=("sign", "signature", "apk"),
                steps=(WorkflowStepSpec("run", "apksigner", {"command": ["apksigner"]}),),
            )
        )

    def register(self, workflow: WorkflowDefinition) -> None:
        self._workflows[workflow.name] = workflow

    def get(self, name: str) -> Optional[WorkflowDefinition]:
        return self._workflows.get(name)

    def all(self) -> List[WorkflowDefinition]:
        return list(self._workflows.values())

    def match_request(self, request: str) -> Optional[WorkflowDefinition]:
        request_lower = request.lower()
        best: Optional[WorkflowDefinition] = None
        best_score = 0

        for workflow in self._workflows.values():
            score = sum(1 for keyword in workflow.keywords if keyword in request_lower)
            if score > best_score:
                best = workflow
                best_score = score

        return best if best_score > 0 else None
