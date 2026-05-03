import threading
from creational_patterns.singleton import InventoryDBConnection


def test_singleton_thread_safety():
    instances = []

    def worker():
        instances.append(InventoryDBConnection.instance("db://thread"))

    threads = [threading.Thread(target=worker) for _ in range(30)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(instances) == 30
    first = instances[0]
    assert all(i is first for i in instances)