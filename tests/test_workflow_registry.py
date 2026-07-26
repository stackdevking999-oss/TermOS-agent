from termos_agent.core.workflow_registry import WorkflowRegistry


def test_workflow_registry_matches_known_apk_decode():
    registry = WorkflowRegistry()
    workflow = registry.match_request("decode this apk")
    assert workflow is not None
    assert workflow.name == "decode_apk"
    assert workflow.skill_name == "decode_apk"


def test_workflow_registry_matches_health_request():
    registry = WorkflowRegistry()
    workflow = registry.match_request("health check")
    assert workflow is not None
    assert workflow.name == "health_check"
