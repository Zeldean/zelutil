from pathlib import Path

def resolve_state_dir():
    """Resolve the shared state directory for all zel apps."""
    return Path.home() / ".local" / "state" / "zel"
