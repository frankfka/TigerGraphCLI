from tgcli.util import cli
from tgcli.util.tgcli_config import get_configs, TgcliConfigurationError


def list_configs():
    """Lists all available configurations with their names and servers"""
    try:
        configs = get_configs(raise_on_nonexistent=True)
    except TgcliConfigurationError as e:
        cli.print_to_console(e.message, is_err=True)
        cli.print_to_console("Please add a valid configuration using tgcli config add", is_err=True)
        return
    cli.print_to_console("Configurations", is_header=True)
    for config in configs.values():
        cli.print_to_console(f"{config.name}: {config.server}")
