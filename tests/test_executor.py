from termos_agent.core.executor import Executor


def test_executor_runs_command():
    result = Executor().run(["python3", "-c", "print('ok')"])
    assert result.returncode == 0
    assert result.stdout.strip() == "ok"
