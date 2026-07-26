from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Optional

from termos_agent.core.feedback import RunFeedback


@dataclass
class RepairSuggestion:
    category: str
    summary: str
    confidence: float
    safe_actions: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)


@dataclass
class RepairResult:
    feedback: RunFeedback
    suggestions: List[RepairSuggestion]
    should_retry: bool
    auto_apply: bool = False


class RepairEngine:
    _patterns = {
        "module_not_found": re.compile(r"ModuleNotFoundError: No module named '([^']+)'"),
        "permission_denied": re.compile(r"PermissionError:|Permission denied", re.IGNORECASE),
        "file_not_found": re.compile(r"FileNotFoundError:|No such file or directory", re.IGNORECASE),
        "command_not_found": re.compile(r"(?:command not found|not recognized as an internal or external command)", re.IGNORECASE),
        "timeout": re.compile(r"timeout|timed out", re.IGNORECASE),
        "sqlite_locked": re.compile(r"database is locked|sqlite_busy", re.IGNORECASE),
        "import_error": re.compile(r"ImportError:|cannot import name", re.IGNORECASE),
    }

    def classify(self, text: str) -> tuple[str, List[str]]:
        matched: List[str] = []
        for name, pattern in self._patterns.items():
            if pattern.search(text):
                matched.append(name)
        category = matched[0] if matched else "unknown"
        return category, matched

    def analyze(self, feedback: RunFeedback) -> RepairResult:
        haystack = "\n".join(
            [feedback.stdout or "", feedback.stderr or "", feedback.notes or "", str(feedback.metadata or {})]
        )
        category, matched = self.classify(haystack)

        suggestions: List[RepairSuggestion] = []
        should_retry = False

        if category == "module_not_found" or category == "import_error":
            missing = self._extract_missing_module(haystack)
            suggestions.append(
                RepairSuggestion(
                    category=category,
                    summary=f"A module import failed: {missing or 'unknown module'}.",
                    confidence=0.96,
                    safe_actions=[
                        "confirm the module path exists in the repository",
                        "confirm the package is included in pyproject.toml",
                        "add the missing file or fix the import path",
                    ],
                    evidence=matched,
                )
            )
            should_retry = True

        elif category == "permission_denied":
            suggestions.append(
                RepairSuggestion(
                    category=category,
                    summary="A permission issue blocked the run.",
                    confidence=0.9,
                    safe_actions=[
                        "inspect file and directory permissions",
                        "verify the target path is writable",
                        "avoid destructive permission changes until the exact path is known",
                    ],
                    evidence=matched,
                )
            )
            should_retry = False

        elif category == "file_not_found":
            suggestions.append(
                RepairSuggestion(
                    category=category,
                    summary="A referenced file or path could not be found.",
                    confidence=0.9,
                    safe_actions=[
                        "verify the manifest path",
                        "verify the repository path",
                        "check whether the file should be created or whether the path is wrong",
                    ],
                    evidence=matched,
                )
            )
            should_retry = True

        elif category == "command_not_found":
            suggestions.append(
                RepairSuggestion(
                    category=category,
                    summary="A shell command was missing from the environment.",
                    confidence=0.88,
                    safe_actions=[
                        "check whether the tool is installed",
                        "check PATH",
                        "use a documented fallback tool if one exists",
                    ],
                    evidence=matched,
                )
            )
            should_retry = True

        elif category == "timeout":
            suggestions.append(
                RepairSuggestion(
                    category=category,
                    summary="The task exceeded the allowed runtime.",
                    confidence=0.8,
                    safe_actions=[
                        "split the task into smaller steps",
                        "increase timeout only after confirming the command is progressing",
                        "inspect logs for an infinite loop or network stall",
                    ],
                    evidence=matched,
                )
            )
            should_retry = True

        elif category == "sqlite_locked":
            suggestions.append(
                RepairSuggestion(
                    category=category,
                    summary="SQLite was locked by another writer.",
                    confidence=0.84,
                    safe_actions=[
                        "ensure one writer at a time",
                        "retry after a short delay",
                        "keep feedback writes serialized",
                    ],
                    evidence=matched,
                )
            )
            should_retry = True

        else:
            suggestions.append(
                RepairSuggestion(
                    category="unknown",
                    summary="No known failure pattern matched.",
                    confidence=0.35,
                    safe_actions=[
                        "inspect the full traceback",
                        "capture the environment snapshot",
                        "add a new classifier once the pattern repeats",
                    ],
                    evidence=matched,
                )
            )

        repair_feedback = RunFeedback(
            kind="repair",
            name=feedback.name,
            status="diagnosed" if category != "unknown" else "needs-review",
            environment=feedback.environment,
            command=feedback.command,
            stdout=feedback.stdout,
            stderr=feedback.stderr,
            exit_code=feedback.exit_code,
            runtime_seconds=feedback.runtime_seconds,
            artifacts=list(feedback.artifacts),
            notes=" | ".join(s.summary for s in suggestions),
            metadata={
                "category": category,
                "matched_patterns": matched,
                "source_kind": feedback.kind,
            },
        )
        return RepairResult(
            feedback=repair_feedback,
            suggestions=suggestions,
            should_retry=should_retry,
            auto_apply=False,
        )

    @staticmethod
    def _extract_missing_module(text: str) -> Optional[str]:
        match = re.search(r"ModuleNotFoundError: No module named '([^']+)'", text)
        if match:
            return match.group(1)
        return None
