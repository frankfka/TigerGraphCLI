import configparser
from typing import Dict, Tuple

from util.io import CONFIG_FILEPATH, CREDENTIALS_FILEPATH, APP_DIR

# Keys
CONFIG_SERVER_KEY = "server"
CONFIG_CLIENT_VERSION_KEY = "client_version"
CREDENTIALS_USERNAME_KEY = "username"
CREDENTIALS_PASSWORD_KEY = "password"


class TgcliConfiguration:

    def __init__(self, name: str, server: str, username: str, password: str, client_version: str):
        self.name: str = name
        self.server: str = server
        self.username: str = username
        self.password: str = password
        self.client_version: str = client_version

    def to_config_parser_dicts(self) -> Tuple[Dict, Dict]:
        conf = {
            CONFIG_SERVER_KEY: self.server,
            CONFIG_CLIENT_VERSION_KEY: self.client_version
        }
        creds = {
            CREDENTIALS_USERNAME_KEY: self.username,
            CREDENTIALS_PASSWORD_KEY: self.password,
        }
        return conf, creds

    @classmethod
    def from_config_parser(cls, name: str, config_section: configparser.SectionProxy):
        return cls(
            name=name,
            server=config_section.get(CONFIG_SERVER_KEY, "").__str__(),
            client_version=config_section.get(CONFIG_CLIENT_VERSION_KEY, "").__str__(),
            username=config_section.get(CREDENTIALS_USERNAME_KEY, "").__str__(),
            password=config_section.get(CREDENTIALS_PASSWORD_KEY, "").__str__()
        )


class TgcliConfigurationError(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def __read_config_files__(raise_on_nonexistent: bool = False) -> Dict[str, TgcliConfiguration]:
    if not (CONFIG_FILEPATH.exists() and CREDENTIALS_FILEPATH.exists()):
        if raise_on_nonexistent:
            raise TgcliConfigurationError(
                message="No valid configuration files exist.")  # TODO: help text for cli prompt
        else:
            return {}
    config = configparser.ConfigParser()
    config.read([CONFIG_FILEPATH, CREDENTIALS_FILEPATH])
    cli_configs: Dict[str, TgcliConfiguration] = {}
    for config_name in config.sections():
        cli_configs[config_name] = TgcliConfiguration.from_config_parser(config_name, config[config_name])
    return cli_configs


def save_configs(configs: Dict[str, TgcliConfiguration]):
    combined_config = configparser.ConfigParser()
    combined_credentials = configparser.ConfigParser()
    for name, conf in configs.items():
        conf_dict, creds_dict = conf.to_config_parser_dicts()
        combined_config[name] = conf_dict
        combined_credentials[name] = creds_dict
    APP_DIR.mkdir(parents=False, exist_ok=True)
    with open(CONFIG_FILEPATH, 'w') as f:
        combined_config.write(f, space_around_delimiters=False)
    with open(CREDENTIALS_FILEPATH, 'w') as f:
        combined_credentials.write(f, space_around_delimiters=False)


def get_configs(raise_on_nonexistent=False) -> Dict[str, TgcliConfiguration]:
    return __read_config_files__(raise_on_nonexistent=raise_on_nonexistent)


def add_config(config: TgcliConfiguration):
    # Get all configs and add to the dict, replacing any existing items
    configs = __read_config_files__()
    configs[config.name] = config
    save_configs(configs)
