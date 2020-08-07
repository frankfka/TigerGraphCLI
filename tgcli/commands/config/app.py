import typer

from tgcli.commands.config.add import add_config
from tgcli.commands.config.delete import delete_config
from tgcli.commands.config.describe import describe_config
from tgcli.commands.config.list import list_configs

config_app = typer.Typer()


@config_app.command(name="add")
def add_config_command():
    add_config()


@config_app.command(name="list")
def list_configs_command():
    list_configs()


@config_app.command(name="describe")
def describe_config_command(
        config_name: str,
        show_password: bool = typer.Option(False, "--show-password", help="Whether to show password in output.")
):
    describe_config(config_name=config_name, show_password=show_password)


@config_app.command(name="delete")
def delete_config_command(name: str):
    delete_config(name)
