import platform
from kommander.context import get_os_info

def test_get_os_info_returns_dict():
    """
    Tests if the get_os_info function returns a dictionary.
    """
    info = get_os_info()
    assert isinstance(info, dict)

def test_get_os_info_contains_os_family():
    """
    Tests if the returned dictionary contains the 'os_family' key
    and that its value matches the current system.
    """
    info = get_os_info()
    assert "os_family" in info
    assert info["os_family"] == platform.system()

def test_get_os_info_contains_architecture():
    """
    Tests if the returned dictionary contains the 'architecture' key
    and that its value matches the current system architecture.
    """
    info = get_os_info()
    assert "architecture" in info
    assert info["architecture"] == platform.machine()
