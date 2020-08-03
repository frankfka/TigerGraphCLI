from util import cli
from util.tgcli_config import get_configs, TgcliConfigurationError


def list_configs():
    try:
        configs = get_configs(raise_on_nonexistent=True)
    except TgcliConfigurationError as e:
        cli.print_to_console(e.message, is_err=True)
        return
    cli.print_to_console("Configurations")
    for config in configs.values():
        cli.print_to_console(f"{config.name}: {config.server}")
