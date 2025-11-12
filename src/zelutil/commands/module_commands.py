import sys
import click

from ..core.installer import clone_module, install_modules
from ..core.registry import load_modules, validate_module, get_module_names
from ..core.updater import update_modules

@click.group()
def module():
    """Manage all zel modules"""
    pass

@module.command("get")
@click.argument("module")
def get_module(module):
    """Clone a module to the installation directory"""
    modules = load_modules()
    if not validate_module(module):
        available = ", ".join(sorted(get_module_names()))
        click.echo(f"Error: Module '{module}' not found.", err=True)
        click.echo(f"Available modules: {available}", err=True)
        sys.exit(1)

    module_info = modules[module]
    success, message = clone_module(module, module_info["git_url"])
    
    if success:
        click.echo(f"✅ {message}")
    else:
        click.echo(f"❌ {message}", err=True)
        sys.exit(1)

@module.command("install")
def install_module():
    """Install all zel modules"""
    modules = load_modules()
    if not modules:
        click.echo("No modules configured.")
        return
    
    success = install_modules(modules)
    if success:
        click.echo("✅ All modules installed successfully")
    else:
        click.echo("❌ Installation failed", err=True)

@module.command("update")
def update_all():
    """Update all installed zel modules"""
    updated, failed, error = update_modules()
    
    if error:
        click.echo(error)
        return
    
    if updated:
        click.echo(f"✅ Updated: {', '.join(updated)}")
        click.echo("Reinstalling updated modules...")
        install_module.callback()
    
    if failed:
        for module, error_msg in failed:
            click.echo(f"❌ Failed to update {module}: {error_msg}", err=True)
    
    if not updated and not failed:
        click.echo("No modules found to update.")