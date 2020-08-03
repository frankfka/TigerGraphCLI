from util import cli
from util.tgcli_config import get_configs, TgcliConfigurationError


def describe_config(config_name: str, show_password: bool):
    configs = {}
    try:
        configs = get_configs(raise_on_nonexistent=True)
    except TgcliConfigurationError as e:
        cli.terminate(message=e.message, is_err=True)
    config = configs.get(config_name, None)
    if not config:
        cli.terminate(message=f"Configuration {config_name} not found.", is_err=True)
    cli.print_to_console(f"Configuration {config_name}")
    # Print configuration values
    cli.print_to_console(f"Server: {config.server}")
    cli.print_to_console(f"Client Version: {config.client_version}")
    cli.print_to_console(f"Username: {config.username}")
    password = "*****"
    if show_password:
        password = config.password
    cli.print_to_console(f"Password: {password}")
