from ..core.registry import load_modules
from ..core.installer import get_install_dir


def get_installed_apps():
    """Get list of installed Zel apps"""
    install_dir = get_install_dir()
    modules = load_modules()
    
    installed = []
    for module_name in modules.keys():
        if (install_dir / module_name).exists():
            installed.append(module_name)
    
    return installed


def get_app_data_dir(app_name):
    """Get data directory for a specific app"""
    from .state import resolve_state_dir
    return resolve_state_dir() / app_name