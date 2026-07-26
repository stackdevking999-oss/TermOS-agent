from pathlib import Path
import sqlite3
from typing import Any, Dict, List


class MemoryStore:
    def __init__(self, path: str = "storage/termos_agent.sqlite3") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS environment_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_json TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS test_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    feedback_json TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def record_task(self, task: str, success: bool, message: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO task_runs(task, success, message) VALUES (?, ?, ?)",
                (task, int(success), message),
            )
            conn.commit()

    def record_environment(self, profile_json: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO environment_profiles(profile_json) VALUES (?)",
                (profile_json,),
            )
            conn.commit()

    def record_test_run(self, test_name: str, status: str, feedback_json: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO test_runs(test_name, status, feedback_json) VALUES (?, ?, ?)",
                (test_name, status, feedback_json),
            )
            conn.commit()
