import click
from .paths import get_path, set_path
from .state import resolve_state_dir
from .registry import get_available_paths, get_path_info, suggest_paths

@click.group()
def main():
    """ZelCandy — Shared configuration for Zel CLI tools."""
    pass

@main.group()
def path():
    """Manage paths."""
    pass

@path.command("set")
@click.argument("key")
@click.argument("value")
def set_path_cmd(key, value):
    """Set a path."""
    set_path(key, value)
    click.echo(f"Set {key} = {value}")

@path.command("get")
@click.argument("key")
def get_path_cmd(key):
    """Get a path."""
    try:
        value = get_path(key)
        click.echo(value)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)

@path.command("list")
def list_paths():
    """List all configured paths."""
    import json
    paths_file = resolve_state_dir() / "paths.json"
    if paths_file.exists():
        with open(paths_file) as f:
            paths = json.load(f)
            for key, value in paths.items():
                click.echo(f"{key}: {value}")
    else:
        click.echo("No paths configured")

@path.command("available")
def available_paths():
    """Show available path keys."""
    click.echo("Available path keys:")
    for key in get_available_paths():
        info = get_path_info(key)
        click.echo(f"  {key}: {info.get('description', 'No description')}")
        click.echo(f"    Example: {info.get('example', 'N/A')}")
        click.echo(f"    Used by: {', '.join(info.get('used_by', []))}")
        click.echo()
