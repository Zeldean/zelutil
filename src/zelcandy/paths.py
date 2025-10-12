import json
from pathlib import Path
from .state import resolve_state_dir

def get_path(key, cli_override=None, save_if_override=False, default=None):
    """Get path from paths.json with override and save options."""
    if cli_override:
        if save_if_override:
            set_path(key, cli_override)
        return cli_override
    
    paths_file = resolve_state_dir() / "paths.json"
    if paths_file.exists():
        with open(paths_file) as f:
            paths = json.load(f)
            if key in paths:
                return paths[key]
    
    if default:
        return default
    
    raise ValueError(f"Path '{key}' not found. Use --save-path to set it.")

def set_path(key, value):
    """Set a path in paths.json."""
    state_dir = resolve_state_dir()
    state_dir.mkdir(parents=True, exist_ok=True)
    
    paths_file = state_dir / "paths.json"
    paths = {}
    if paths_file.exists():
        with open(paths_file) as f:
            paths = json.load(f)
    
    paths[key] = str(value)
    with open(paths_file, 'w') as f:
        json.dump(paths, f, indent=2)
