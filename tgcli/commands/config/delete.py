from tgcli.util import cli
from tgcli.tigergraph.common import delete_dependencies
from tgcli.util.tgcli_config import get_configs, TgcliConfigurationError, save_configs


def delete_config(name: str):
    """Delete a configuration with the given name."""
    try:
        all_configs = get_configs(raise_on_nonexistent=True)
    except TgcliConfigurationError as e:
        # No configuration files found - or error while retrieving the files
        cli.print_to_console(e.message, is_err=True)
        cli.print_to_console("Please add a valid configuration using tgcli config add", is_err=True)
        return
    if not all_configs[name]:
        cli.print_to_console(f"Configuration {name} not found.", is_err=True)
        return
    if cli.get_input_bool(f"Are you sure you want to delete {name}?"):
        # Delete all the associated initialization files
        delete_dependencies(all_configs[name])
        # Delete the dictionary associated with the config
        del all_configs[name]
        save_configs(all_configs)
        cli.print_to_console(f"{name} deleted.")
