"""
Main Typer app for root commands
"""
from pathlib import Path

import typer

from commands.config.app import config_app
from commands.main.delete.app import delete_app
from commands.main.get.app import get_app
from commands.main.load.app import load_app
from commands.main.util import get_initialized_tg_connection
from util import cli

main_app = typer.Typer()

# Config
main_app.add_typer(typer_instance=config_app, name="config")

# Load
main_app.add_typer(typer_instance=load_app, name="load")

# Get
main_app.add_typer(typer_instance=get_app, name="get")

# Delete
main_app.add_typer(typer_instance=delete_app, name="delete")


@main_app.command("echo")
def echo(config_name: str):
    """
    Pings the TigerGraph server associated with the configuration
    """
    conn = get_initialized_tg_connection(config_name=config_name, graph_name="")
    cli.print_to_console(conn.echo())


@main_app.command("reinit-dependencies")
def reinit_dependencies(config_name: str):
    """
    Force download dependencies and generate a new secret
    TODO: this doesn't seem to work
    """
    conn = get_initialized_tg_connection(config_name=config_name, graph_name="", clean_init=True)
    cli.print_to_console(conn.echo())


@main_app.command("gsql")
def gsql(
        config_name: str,
        graph_name: str = typer.Argument(None, help="Graph to query"),
        gsql_command: str = typer.Option(None, "--command", help="Inline GSQL command")
):
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name)
    options = []
    # TODO: Validate that a command is going to be run
    if graph_name:
        options = ["-g", graph_name]
    # TODO: Allow for editor execution, file execution, etc.
    output = conn.gsql(gsql_command, options=options)
    cli.print_to_console(output)
