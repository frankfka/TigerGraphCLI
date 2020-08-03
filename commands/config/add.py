import re

import util.cli as cli
from util.tgcli_config import TgcliConfiguration, get_configs, save_configs


def __clean_config_name__(name: str) -> str:
    return re.sub(r'\W+', '', name)


def add_config():
    # TODO: Allow for programmatic
    new_config = __get_config_interactive__()
    curr_configs = get_configs()
    if curr_configs.get(new_config.name, None):
        cli.print_to_console(f"Configuration {new_config.name} already exists. "
                             f"To replace it, please delete the configuration first.")
        return
    curr_configs[new_config.name] = new_config
    save_configs(curr_configs)
    cli.print_to_console(f"Configuration {new_config.name} added for server {new_config.server}")


def __get_config_interactive__() -> TgcliConfiguration:
    # TODO: validation
    cli.print_to_console("Adding a TigerGraph configuration")
    server_address = cli.get_input_str("Server Address (ex. https://xyz.i.tgcloud.io").strip()
    client_version = cli.get_input_str("Client Version (ex. 3.0.0)").strip()
    server_username = cli.get_input_str("Username").strip()
    server_password = cli.get_input_str("Password", hide_input=True)
    name = cli.get_input_str("Name (Alphanumeric & Underscore Allowed)").strip()
    name = __clean_config_name__(name)
    return TgcliConfiguration(
        name=name,
        server=server_address,
        username=server_username,
        password=server_password,
        client_version=client_version
    )
