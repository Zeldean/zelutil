import json
import click

from ..utils.state import resolve_state_dir
from ..core.registry import get_module_names, load_modules


@click.group()
def manage():
    """Manage zel configuration"""
    pass


@manage.command("list")
def list_modules():
    """List available zel modules"""
    modules = load_modules()
    if not modules:
        click.echo("No modules configured.")
        return

    click.echo("Available zel modules:")
    for name, info in modules.items():
        click.echo(f"  • {name} - {info['description']}")


@manage.command("paths")
def list_paths():
    """List all configured paths"""
    paths_file = resolve_state_dir() / "paths.json"
    if paths_file.exists():
        with open(paths_file) as f:
            paths = json.load(f)
            for key, value in paths.items():
                click.echo(f"{key}: {value}")
    else:
        click.echo("No paths configured")