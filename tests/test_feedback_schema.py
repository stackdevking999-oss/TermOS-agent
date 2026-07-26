import json
from pathlib import Path


def test_feedback_schema_contains_required_fields():
    schema_path = Path("config/test_feedback.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema["title"] == "TermOS agent Test Feedback"
    required = set(schema["required"])
    for field in [
        "test_name",
        "status",
        "environment",
        "command",
        "stdout",
        "stderr",
        "exit_code",
        "runtime_seconds",
        "artifacts",
        "notes",
    ]:
        assert field in required
