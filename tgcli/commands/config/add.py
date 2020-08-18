import re

from tgcli.util import cli
from tgcli.util.tgcli_config import TgcliConfiguration, get_configs, save_configs, DEFAULT_RESTPP_PORT, DEFAULT_GS_PORT


def __clean_config_name__(name: str) -> str:
    """Only allow alphanumeric and underscores in the name"""
    return re.sub(r'\W+', '', name)


def add_config():
    """Adds a configuration - only supports interactive input for now"""
    new_config = __get_config_interactive__()
    curr_configs = get_configs()
    if curr_configs.get(new_config.name, None):
        # Make sure that we want to overwrite
        if not cli.get_input_bool(
                prompt=f"Configuration {new_config.name} already exists. Do you want to overwrite it?"
        ):
            cli.terminate(message="Add configuration cancelled.")
        # Overwriting a configuration may need a reinitialization of dependencies
        cli.print_to_console(f"Configuration {new_config.name} already exists. You may need to run "
                             f"tgcli reinit-dependencies to update dependencies to reflect this new configuration.")
    curr_configs[new_config.name] = new_config
    save_configs(curr_configs)
    cli.print_to_console(f"Configuration {new_config.name} added for server {new_config.server}")


def __get_config_interactive__() -> TgcliConfiguration:
    """Retrieves a configuration from the user interactively

    :return: A TgcliConfiguration that corresponds to the input
    """
    cli.print_to_console("Adding a TigerGraph configuration")
    server_address = cli.get_input_str("Server Address (ex. https://xyz.i.tgcloud.io)").strip()
    client_version = cli.get_input_str("Client Version (3.0.0, 2.6.0, 2.5.2, 2.5.0, 2.4.1, 2.4.0, 2.3.2)").strip()
    restpp_port = cli.get_input_str("REST++ Port", default=DEFAULT_RESTPP_PORT).strip()
    gs_port = cli.get_input_str("GS Port", default=DEFAULT_GS_PORT).strip()
    use_auth = cli.get_input_bool("Use Auth (This is usually true)", default=True)
    server_username = cli.get_input_str("Username", default="tigergraph").strip()
    server_password = cli.get_input_str("Password", default="tigergraph", hide_input=True)
    name = cli.get_input_str("Name (Alphanumeric & Underscore Allowed)").strip()
    name = __clean_config_name__(name)
    return TgcliConfiguration(
        name=name,
        server=server_address,
        username=server_username,
        password=server_password,
        client_version=client_version,
        restpp_port=restpp_port,
        gs_port=gs_port,
        use_auth=use_auth
    )
