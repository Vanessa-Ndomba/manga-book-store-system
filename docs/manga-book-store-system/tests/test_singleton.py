from creational_patterns.singleton import InventoryDBConnection


def test_singleton_same_instance():
    a = InventoryDBConnection.instance("db://one")
    b = InventoryDBConnection.instance("db://two")
    assert a is b
    assert a.dsn == "db://one"
