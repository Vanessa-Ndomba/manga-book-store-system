"""Unit tests for the Singleton pattern (DatabaseConnection)."""
import threading
import pytest
from creational_patterns.singleton.database_connection import DatabaseConnection


class TestDatabaseConnectionSingleton:
    """Tests for the DatabaseConnection singleton."""

    def setup_method(self):
        """Reset singleton state before each test to ensure isolation."""
        DatabaseConnection.reset()

    def test_returns_same_instance(self):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2

    def test_same_instance_with_different_params(self):
        """Constructor args after first instantiation are ignored (singleton contract)."""
        db1 = DatabaseConnection(host="localhost", database="manga_db")
        db2 = DatabaseConnection(host="other-host", database="other_db")
        assert db1 is db2

    def test_initial_state_not_connected(self):
        db = DatabaseConnection()
        assert db.is_connected is False

    def test_connect_sets_connected_true(self):
        db = DatabaseConnection()
        db.connect()
        assert db.is_connected is True
        db.disconnect()

    def test_disconnect_sets_connected_false(self):
        db = DatabaseConnection()
        db.connect()
        db.disconnect()
        assert db.is_connected is False

    def test_double_connect_is_idempotent(self):
        db = DatabaseConnection()
        db.connect()
        db.connect()  # Should not raise
        assert db.is_connected is True
        db.disconnect()

    def test_execute_query_requires_connection(self):
        db = DatabaseConnection()
        with pytest.raises(RuntimeError, match="not connected"):
            db.execute_query("SELECT 1")

    def test_execute_query_when_connected(self):
        db = DatabaseConnection()
        db.connect()
        result = db.execute_query("SELECT * FROM manga")
        assert isinstance(result, list)
        db.disconnect()

    def test_query_count_increments(self):
        db = DatabaseConnection()
        db.connect()
        initial = db.query_count
        db.execute_query("SELECT 1")
        db.execute_query("SELECT 2")
        assert db.query_count == initial + 2
        db.disconnect()

    def test_host_property(self):
        db = DatabaseConnection(host="db.manga.local")
        assert db.host == "db.manga.local"

    def test_database_property(self):
        db = DatabaseConnection(database="mangastore")
        assert db.database == "mangastore"

    def test_repr_includes_status(self):
        db = DatabaseConnection()
        assert "disconnected" in repr(db)
        db.connect()
        assert "connected" in repr(db)
        db.disconnect()

    # ── Thread-safety tests ───────────────────────────────────────────────────

    def test_singleton_thread_safety(self):
        """Multiple threads must receive the same instance."""
        instances: list[DatabaseConnection] = []
        lock = threading.Lock()

        def get_instance():
            instance = DatabaseConnection()
            with lock:
                instances.append(instance)

        threads = [threading.Thread(target=get_instance) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(instances) == 20
        first = instances[0]
        assert all(inst is first for inst in instances), (
            "All threads should receive the same DatabaseConnection instance"
        )

    def test_reset_allows_new_instance(self):
        db1 = DatabaseConnection()
        DatabaseConnection.reset()
        db2 = DatabaseConnection()
        # After reset, a new instance is created
        assert db2 is not db1
