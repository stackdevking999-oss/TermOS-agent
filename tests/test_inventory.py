from termos_agent.environment.inventory import Inventory


def test_inventory_has_basic_fields():
    profile = Inventory().as_dict()
    assert "system" in profile
    assert "machine" in profile
    assert "python" in profile
    assert "tools" in profile
