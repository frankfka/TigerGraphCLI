"""
Main Typer app for root commands
"""
from pathlib import Path

import typer

from commands.config.app import config_app
from commands.main.load.app import load_app
from commands.main.util import get_initialized_tg_connection
from tigergraph.common import get_tg_connection
from util.tgcli_config import get_configs
from util import cli

main_app = typer.Typer()

# Config
main_app.add_typer(typer_instance=config_app, name="config")

# Load
main_app.add_typer(typer_instance=load_app, name="load")

# TODO: Delete

# TODO: get

# TODO: Start server and make sure all works apikey
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
