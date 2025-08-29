import platform
from typing import Dict, Any

def get_os_info() -> Dict[str, Any]:
    """
    Gathers basic information about the host operating system.

    For v0.1, this focuses on identifying the OS family (Linux, Darwin, Windows).
    This will be expanded later to include distribution, version, and package manager.

    Returns:
        A dictionary containing basic OS information.
    """
    system = platform.system()
    
    # We can add more details here later
    os_info = {
        "os_family": system,
        "architecture": platform.machine(),
    }
    
    return os_info
