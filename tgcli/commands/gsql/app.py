from pathlib import Path

import typer

from tgcli.commands.etc.help_text import CONFIG_ARG_HELP, GRAPH_ARG_HELP
from tgcli.commands.util import get_initialized_tg_connection
from tgcli.util import cli

gsql_app = typer.Typer(help="Run GSQL commands against a TigerGraph server.")


@gsql_app.command("run")
def run_gsql(
        config_name: str = typer.Argument(None, help=CONFIG_ARG_HELP),
        graph_name: str = typer.Argument(None, help=GRAPH_ARG_HELP),
        inline_command: str = typer.Option(None, "--command", help="Inline GSQL command"),
        file_command: Path = typer.Option(
            None, "--file", help="Filepath to load a GSQL command from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        ),
        launch_editor: bool = typer.Option(
            False, "--editor", help="Launch an interactive editor to load the GSQL command"
        )
):
    """Run a GSQL query against a configuration through an inline command, file, or interactive editor"""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name)
    options = []
    if graph_name:
        options = ["-g", graph_name]
    command = None
    # Get the GSQL command depending on the flag
    if inline_command:
        command = inline_command
    elif file_command:
        with open(file_command, "r") as cmd_file:
            command = cmd_file.read()
    elif launch_editor:
        command = cli.get_input_from_editor("")
    command = command.strip()
    if not command:
        cli.terminate(message="No command specified.", is_err=True)
    output = conn.gsql(command, options=options)
    cli.print_to_console(output)
