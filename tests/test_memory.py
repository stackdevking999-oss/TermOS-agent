from termos_agent.core.memory import MemoryStore


def test_memory_initializes_schema(tmp_path):
    db_path = tmp_path / "termos.sqlite3"
    store = MemoryStore(str(db_path))
    store.init_schema()
    store.record_task("demo", True, "ok")
    assert db_path.exists()
