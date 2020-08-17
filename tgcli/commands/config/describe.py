from tgcli.util import cli
from tgcli.util.tgcli_config import get_configs, TgcliConfigurationError


def describe_config(config_name: str, show_sensitive: bool):
    """Output all the parameters from a TgcliConfiguration, optionally showing sensitive data."""
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
    cli.print_to_console(f"Client Version: {config.client_version}")  # TODO: List v3_0_0 v2_6_0 v2_5_2 v2_5_0 v2_4_1 v2_4_0 v2_3_2
    cli.print_to_console(f"REST++ Port: {config.restpp_port}")
    cli.print_to_console(f"GS Port: {config.gs_port}")
    cli.print_to_console(f"Use Auth: {config.use_auth}")
    cli.print_to_console(f"Username: {config.username}")
    password = "*****"
    secret = "*****"
    if show_sensitive:
        password = config.password
        secret = config.secret
    cli.print_to_console(f"Password: {password}")
    cli.print_to_console(f"Secret: {secret}")
