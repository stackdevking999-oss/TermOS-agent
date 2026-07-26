from termos_agent.core.feedback import RunFeedback
from termos_agent.core.repair import RepairEngine


def test_repair_engine_classifies_missing_module():
    feedback = RunFeedback(
        kind="test",
        name="smoke",
        status="failed",
        environment={"system": "Android"},
        command=["python3", "-m", "termos_agent.cli"],
        stdout="",
        stderr="Traceback (most recent call last):\nModuleNotFoundError: No module named 'termos_agent.environment.capabilities'",
        exit_code=1,
        runtime_seconds=0.1,
        notes="import failure",
        metadata={},
    )
    result = RepairEngine().analyze(feedback)
    assert result.feedback.kind == "repair"
    assert result.feedback.metadata["category"] == "module_not_found"
    assert result.should_retry is True
    assert result.suggestions
    assert any("module path" in action for action in result.suggestions[0].safe_actions)
