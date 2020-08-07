import re

from tgcli.util import cli
from tgcli.util.tgcli_config import TgcliConfiguration, get_configs, save_configs, DEFAULT_RESTPP_PORT, DEFAULT_GS_PORT


def __clean_config_name__(name: str) -> str:
    return re.sub(r'\W+', '', name)


def add_config():
    # TODO: Allow for programmatic
    new_config = __get_config_interactive__()
    curr_configs = get_configs()
    if curr_configs.get(new_config.name, None):
        # Prevent updates for now - will need to reinit dependencies, leaving as TODO
        cli.print_to_console(f"Configuration {new_config.name} already exists. "
                             f"To replace it, please delete the configuration first.")
        return
    curr_configs[new_config.name] = new_config
    save_configs(curr_configs)
    cli.print_to_console(f"Configuration {new_config.name} added for server {new_config.server}")


def __get_config_interactive__() -> TgcliConfiguration:
    # TODO: validation, defaults
    cli.print_to_console("Adding a TigerGraph configuration")
    server_address = cli.get_input_str("Server Address (ex. https://xyz.i.tgcloud.io").strip()
    client_version = cli.get_input_str("Client Version (ex. 3.0.0)").strip()  # TODO: give valid versions
    restpp_port = cli.get_input_str("REST++ Port", default=DEFAULT_RESTPP_PORT).strip()
    gs_port = cli.get_input_str("GS Port", default=DEFAULT_GS_PORT).strip()
    use_auth = cli.get_input_bool("Use Auth (This is usually true)", default=True)
    server_username = cli.get_input_str("Username", default="tigergraph").strip()
    server_password = cli.get_input_str("Password", default="tigergraph", hide_input=True)
    secret = cli.get_input_str(
        "Secret (Autogenerated if this is blank & authentication is enabled)", default="", hide_input=True
    )
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
        use_auth=use_auth,
        secret=secret
    )