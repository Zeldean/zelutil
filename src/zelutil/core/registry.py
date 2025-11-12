import json
from functools import lru_cache
from importlib import resources


@lru_cache(maxsize=1)
def load_modules():
    """Load module configuration bundled with the package"""
    try:
        with resources.open_text("zelutil.data", "zel-modules.json", encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, ModuleNotFoundError):
        return {}
    except json.JSONDecodeError:
        return {}
    
    return data.get("modules", {})


def get_module_names():
    """Get list of module names"""
    return list(load_modules().keys())


def get_module_info(module_name):
    """Get information about a specific module"""
    modules = load_modules()
    return modules.get(module_name)


def validate_module(module_name):
    """Check if module exists in registry"""
    return module_name in load_modules()


# Path registry for known path keys
PATH_REGISTRY = {
    "vault": {
        "description": "Main vault/second-brain directory",
        "example": "/mnt/Vault/Second-Brain",
        "used_by": ["zeljournal"]
    },
    "budget-data": {
        "description": "Budget data directory", 
        "example": "~/Documents/Budget",
        "used_by": ["zelbudget"]
    },
    "media": {
        "description": "Media files directory",
        "example": "~/Media",
        "used_by": ["zelmedia"]
    },
    "projects": {
        "description": "Projects directory",
        "example": "~/Projects", 
        "used_by": ["zelblock"]
    },
    "timer-logs": {
        "description": "Timer log files directory",
        "example": "~/Documents/Timers",
        "used_by": ["zeltimer"]
    }
}


def get_available_paths():
    """Get list of available path keys"""
    return list(PATH_REGISTRY.keys())


def get_path_info(key):
    """Get information about a path key"""
    return PATH_REGISTRY.get(key, {})