import json
from pathlib import Path

from .state import resolve_state_dir


def load_config(app_name=None):
    """Load configuration for app or global config"""
    state_dir = resolve_state_dir()
    
    if app_name:
        config_file = state_dir / app_name / "config.json"
    else:
        config_file = state_dir / "config.json"
    
    if config_file.exists():
        with open(config_file) as f:
            return json.load(f)
    return {}


def save_config(config, app_name=None):
    """Save configuration for app or global config"""
    state_dir = resolve_state_dir()
    
    if app_name:
        config_dir = state_dir / app_name
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"
    else:
        config_file = state_dir / "config.json"
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)