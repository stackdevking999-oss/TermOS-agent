from termos_agent.core.reasoning import LocalReasoningAdapter
from termos_agent.core.workflow_registry import WorkflowRegistry


def test_reasoning_adapter_resolves_known_workflow_without_llm():
    adapter = LocalReasoningAdapter(WorkflowRegistry())
    decision = adapter.analyze("decode apk project")
    assert decision.needs_llm is False
    assert decision.workflow_name == "decode_apk"
    assert decision.skill_name == "decode_apk"
    assert decision.steps


def test_reasoning_adapter_flags_unknown_request_for_llm():
    adapter = LocalReasoningAdapter(WorkflowRegistry())
    decision = adapter.analyze("invent a new protocol for this")
    assert decision.needs_llm is True
    assert decision.workflow_name == ""
