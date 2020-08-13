"""
Main Typer app for root commands
"""
__version__ = '0.0.1'

import typer

from tgcli.commands.config.app import config_app
from tgcli.commands.delete.app import delete_app
from tgcli.commands.get.app import get_app
from tgcli.commands.gsql.app import gsql_app
from tgcli.commands.load.app import load_app
from tgcli.commands.util import get_initialized_tg_connection
from tgcli.util import cli

main_app = typer.Typer(help="CLI for interacting with TigerGraph.")

# Config
main_app.add_typer(typer_instance=config_app, name="config")

# GSQL
main_app.add_typer(typer_instance=gsql_app, name="gsql")

# Load
main_app.add_typer(typer_instance=load_app, name="load")

# Get
main_app.add_typer(typer_instance=get_app, name="get")

# Delete
main_app.add_typer(typer_instance=delete_app, name="delete")


@main_app.command("reinit-dependencies")
def reinit_dependencies(config_name: str):
    """Force download dependencies and generate a new secret for the configuration"""
    _ = get_initialized_tg_connection(config_name=config_name, graph_name="", clean_init=True)
    cli.print_to_console("Done")


@main_app.command("version")
def version():
    cli.print_to_console(__version__)
