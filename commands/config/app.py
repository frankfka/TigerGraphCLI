import typer

from commands.config.add import add_config
from commands.config.delete import delete_config
from commands.config.list import list_configs
from util.cli import print_to_console

config_app = typer.Typer()


@config_app.command(name="add")
def add_config_command():
    add_config()


@config_app.command(name="list")
def list_configs_command():
    list_configs()


@config_app.command(name="describe")
def describe_config_command():
    # TODO
    print_to_console("describe")


@config_app.command(name="delete")
def delete_config_command(name: str):
    delete_config(name)
