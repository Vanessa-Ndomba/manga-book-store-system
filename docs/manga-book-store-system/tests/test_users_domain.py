from src.users import User, Customer


def test_user_deactivate():
    u = User(user_id="u1", email="a@b.com", display_name="A")
    u.deactivate()
    assert u.active is False


def test_customer_update_profile():
    c = Customer(user_id="c1", email="c@b.com", display_name="C")
    c.update_profile(display_name="New", address="123 Street")
    assert c.display_name == "New"
    assert c.default_shipping_address == "123 Street"
