import json
from pathlib import Path


def test_run_feedback_schema_contains_required_fields():
    schema_path = Path("config/run_feedback.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema["title"] == "TermOS agent Run Feedback"
    required = set(schema["required"])
    for field in [
        "kind",
        "name",
        "status",
        "environment",
        "command",
        "stdout",
        "stderr",
        "exit_code",
        "runtime_seconds",
        "artifacts",
        "notes",
        "metadata",
    ]:
        assert field in required
    assert "test" in schema["properties"]["kind"]["enum"]
