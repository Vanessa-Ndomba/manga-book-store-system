def test_this_will_fail_on_purpose():
    """This test is SUPPOSED to fail for demo purposes"""
    # This assertion is intentionally wrong
    expected = "success"
    actual = "failure"
    assert expected == actual, "This test is intentionally broken for CI/CD demo"