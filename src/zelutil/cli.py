import json
import logging
import subprocess
import sys
from functools import lru_cache
from importlib import resources
from pathlib import Path

import click

from .paths import get_path, set_path
from .registry import get_available_paths, get_path_info
from .state import resolve_state_dir

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def load_modules():
    """Load module configuration bundled with the package."""
    try:
        with resources.open_text("zelutil.data", "zel-modules.json", encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, ModuleNotFoundError):
        return {}
    except json.JSONDecodeError as exc:
        logger.warning("Failed to parse module metadata: %s", exc)
        return {}

    return data.get("modules", {})

def get_module_names():
    """Get list of module names"""
    return list(load_modules().keys())

@click.group()
def main():
    """ZelUtil — Shared configuration for Zel CLI tools."""
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

@main.group()
def install():
    """Install zel modules."""
    pass

@install.command("list")
def list_modules():
    """List available zel modules."""
    modules = load_modules()
    if not modules:
        click.echo("No module metadata available.")
        return

    click.echo("Available zel modules:")
    for name, info in modules.items():
        status = "✓" if info.get("installed_version") else "○"
        click.echo(f"  {status} {name} - {info['description']}")

@install.command("all")
def install_all():
    """Run the main install script to install all zel tools."""
    install_script = Path(__file__).parent / "install.py"
    if install_script.exists():
        click.echo("Running install script...")
        subprocess.run([sys.executable, str(install_script)], check=True)
    else:
        click.echo("Install script not found.")

@install.command("module")
@click.argument("module_name")
def install_module(module_name):
    """Install a specific zel module from GitHub (placeholder)."""
    modules = load_modules()
    module_info = modules.get(module_name)
    if not module_info:
        available = ", ".join(sorted(modules.keys())) or "no modules configured"
        raise click.ClickException(f"Unknown module '{module_name}'. Available: {available}")

    click.echo(f"Installing {module_info['name']} from {module_info['git_url']}...")
    # TODO: Implement GitHub clone and install
    click.echo("GitHub installation not yet implemented.")
