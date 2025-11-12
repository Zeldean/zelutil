import click

from .commands import module, manage

@click.group()
def util():
    """ZelUtil — Shared configuration for Zel CLI tools"""
    pass

# Register command groups
util.add_command(module)
util.add_command(manage)
