import configparser
from dataclasses import dataclass
from typing import Dict, Tuple

from tgcli.util.io import CONFIG_FILEPATH, CREDENTIALS_FILEPATH, APP_DIR

# Keys
CONFIG_SERVER_KEY = "server"
CONFIG_CLIENT_VERSION_KEY = "client_version"
CONFIG_RESTPP_PORT = "restpp_port"
CONFIG_GS_PORT = "gs_port"
CONFIG_USE_AUTH = "use_auth"
CREDENTIALS_USERNAME_KEY = "username"
CREDENTIALS_PASSWORD_KEY = "password"
CREDENTIALS_SECRET_KEY = "secret"

# Default Values
DEFAULT_RESTPP_PORT = '9000'
DEFAULT_GS_PORT = '14240'
DEFAULT_USE_AUTH = True


@dataclass
class TgcliConfiguration:
    name: str
    server: str
    username: str
    password: str
    secret: str
    client_version: str
    restpp_port: str = DEFAULT_RESTPP_PORT
    gs_port: str = DEFAULT_GS_PORT
    use_auth: bool = DEFAULT_USE_AUTH

    def to_config_parser_dicts(self) -> Tuple[Dict, Dict]:
        conf = {
            CONFIG_SERVER_KEY: self.server,
            CONFIG_CLIENT_VERSION_KEY: self.client_version,
            CONFIG_RESTPP_PORT: self.restpp_port,
            CONFIG_GS_PORT: self.gs_port,
            CONFIG_USE_AUTH: self.use_auth.__str__()
        }
        creds = {
            CREDENTIALS_USERNAME_KEY: self.username,
            CREDENTIALS_PASSWORD_KEY: self.password,
            CREDENTIALS_SECRET_KEY: self.secret
        }
        return conf, creds

    @classmethod
    def from_config_parser(cls, name: str, config_section: configparser.SectionProxy):
        # Default use_auth to True
        use_auth = DEFAULT_USE_AUTH
        try:
            use_auth = config_section.getboolean(CONFIG_USE_AUTH)
        except ValueError:
            pass

        return cls(
            name=name,
            server=config_section.get(CONFIG_SERVER_KEY, ""),
            client_version=config_section.get(CONFIG_CLIENT_VERSION_KEY, ""),
            restpp_port=config_section.get(CONFIG_RESTPP_PORT, DEFAULT_RESTPP_PORT).__str__(),
            gs_port=config_section.get(CONFIG_GS_PORT, DEFAULT_GS_PORT).__str__(),
            use_auth=use_auth,
            username=config_section.get(CREDENTIALS_USERNAME_KEY, ""),
            password=config_section.get(CREDENTIALS_PASSWORD_KEY, ""),
            secret=config_section.get(CREDENTIALS_SECRET_KEY, "")
        )


class TgcliConfigurationError(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def __read_config_files__(raise_on_nonexistent: bool = False) -> Dict[str, TgcliConfiguration]:
    if not (CONFIG_FILEPATH.exists() and CREDENTIALS_FILEPATH.exists()):
        if raise_on_nonexistent:
            raise TgcliConfigurationError(
                message="No valid configuration files exist.")
        else:
            return {}
    config = configparser.ConfigParser()
    config.read([CONFIG_FILEPATH, CREDENTIALS_FILEPATH])
    cli_configs: Dict[str, TgcliConfiguration] = {}
    for config_name in config.sections():
        cli_configs[config_name] = TgcliConfiguration.from_config_parser(config_name, config[config_name])
    return cli_configs


def save_configs(configs: Dict[str, TgcliConfiguration]):
    """
    Save the entire dictionary of configurations to file at $HOME/.tgcli/
    """
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
    """
    Retrieve all the configurations saved to config and credentials files in $HOME/.tgcli/
    """
    return __read_config_files__(raise_on_nonexistent=raise_on_nonexistent)


def upsert_config(config: TgcliConfiguration):
    """
    Insert or overwrite configurations with the given config
    """
    configs = __read_config_files__()
    configs[config.name] = config
    save_configs(configs)
