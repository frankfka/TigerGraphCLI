"""Typer app for interacting with TigerGraph CLI configurations

Each configuration holds all the information necessary to establish a connection to a TigerGraph server.
Configurations are stored in $HOME/.tgcli/ in two files: `config` and `credentials`
"""


import typer

from tgcli.commands.config.add import add_config
from tgcli.commands.config.delete import delete_config
from tgcli.commands.config.describe import describe_config
from tgcli.commands.config.list import list_configs
from tgcli.commands.etc.help_text import CONFIG_ARG_HELP

config_app = typer.Typer(help="Manage TigerGraph configurations for tgcli.")


@config_app.command(name="add")
def add_config_command():
    """Adds a TgcliConfiguration interactively"""
    add_config()


@config_app.command(name="list")
def list_configs_command():
    """List all the TgcliConfigurations currently available

    Using this command will print out all the configuration names and their respective servers
    """
    list_configs()


@config_app.command(name="describe")
def describe_config_command(
        config_name: str = typer.Argument(None, help=CONFIG_ARG_HELP),
        show_sensitive: bool = typer.Option(
            False, "--show-sensitive", help="Show password and secrets in output if specified."
        )
):
    """Describe a configuration when given the config name

    This will print all the parameters of the configuration to console,
    """
    describe_config(config_name=config_name, show_sensitive=show_sensitive)


@config_app.command(name="delete")
def delete_config_command(name: str = typer.Argument(None, help=CONFIG_ARG_HELP)):
    """Deletes a configuration when given the config name"""
    delete_config(name)
