"""Path registry for known path keys and their descriptions."""

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
    """Get list of available path keys."""
    return list(PATH_REGISTRY.keys())

def get_path_info(key):
    """Get information about a path key."""
    return PATH_REGISTRY.get(key, {})

def suggest_paths(partial_key=""):
    """Suggest path keys based on partial input."""
    if not partial_key:
        return get_available_paths()
    return [key for key in PATH_REGISTRY.keys() if partial_key.lower() in key.lower()]