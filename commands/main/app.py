"""
Main Typer app for root commands
"""


import typer

from commands.config.app import config_app
from tigergraph.common import get_initialized_tg_connection
from util.tgcli_config import get_configs
import util.cli as cli

main_app = typer.Typer()

# Config
main_app.add_typer(typer_instance=config_app, name="config")


@main_app.command("init")
def init():
    typer.echo("init")


@main_app.command("test-another")
def test_1():
    typer.echo("Test 2!")


@main_app.command("gsql")
def gsql(
        config_name: str,
        graph_name: str = typer.Option(None, "--graph", help="Graph to query"),
        gsql_command: str = typer.Option(None, "--command", help="Inline GSQL command")
):
    config = get_configs().get(config_name, None)
    if not config:
        cli.print_to_console("Invalid configuration. Please provide a valid configuration name.", is_err=True)
        return
    conn = get_initialized_tg_connection(config, graph_name)
    options = []
    if graph_name:
        options = ["-g", graph_name]
    output = conn.gsql(gsql_command, options=options)
    cli.print_to_console(output)
