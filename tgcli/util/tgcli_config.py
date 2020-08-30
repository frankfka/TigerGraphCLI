import configparser
from dataclasses import dataclass, field
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
CREDENTIALS_SECRET_PREFIX = "secret_"  # Secrets are scoped to graph, stored as secret_GRAPHNAME

# Default Values
DEFAULT_RESTPP_PORT = '9000'
DEFAULT_GS_PORT = '14240'
DEFAULT_USE_AUTH = True


class TgcliConfigurationError(Exception):
    """Error associated with any configuration operations"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


@dataclass
class TgcliConfiguration:
    """A configuration object with all parameters needed to connect to a TigerGraph server."""
    name: str  # An alias - not used for connectivity
    server: str  # Host with protocol - ex. https://xyz.i.tgcloud.io
    username: str
    password: str
    client_version: str  # Allowed values: 3.0.0, 2.6.0, 2.5.2, 2.5.0, 2.4.1, 2.4.0, 2.3.2
    secrets: dict = field(default_factory=dict)  # Secrets, keyed by the graph name that they correspond to
    restpp_port: str = DEFAULT_RESTPP_PORT  # https://docs-beta.tigergraph.com/dev/restpp-api/restpp-requests
    gs_port: str = DEFAULT_GS_PORT  # Graphstudio port, defaults to 14240
    use_auth: bool = DEFAULT_USE_AUTH  # Whether to use username & password auth

    def to_config_parser_dicts(self) -> Tuple[Dict, Dict]:
        """Splits the configuration into two data dictionaries - one for configuration and one for credentials.

        :return a tuple of (Config dict, Credentials dict)
        """
        conf = {
            CONFIG_SERVER_KEY: self.server,
            CONFIG_CLIENT_VERSION_KEY: self.client_version,
            CONFIG_RESTPP_PORT: self.restpp_port,
            CONFIG_GS_PORT: self.gs_port,
            CONFIG_USE_AUTH: self.use_auth.__str__()
        }
        creds = {
            CREDENTIALS_USERNAME_KEY: self.username,
            CREDENTIALS_PASSWORD_KEY: self.password
        }
        # Create secrets dict and merge it with credentials
        secrets = {}
        for graph_name, secret in self.secrets.items():
            secrets[CREDENTIALS_SECRET_PREFIX + graph_name] = secret
        creds = {**creds, **secrets}
        return conf, creds

    @classmethod
    def from_config_parser(cls, name: str, config_section: configparser.SectionProxy):
        """Parse a configuration from a configparser section"""

        # Default use_auth to True
        use_auth = DEFAULT_USE_AUTH
        try:
            use_auth = config_section.getboolean(CONFIG_USE_AUTH)
        except ValueError:
            pass

        # Get all secrets
        secrets = {}
        for config_key, config_val in config_section.items():
            if config_key.startswith(CREDENTIALS_SECRET_PREFIX):
                # Of form "secret_GRAPHNAME" - parse GRAPHNAME
                graph_name = config_key.replace(CREDENTIALS_SECRET_PREFIX, "", 1)
                secrets[graph_name] = config_val

        return cls(
            name=name,
            server=config_section.get(CONFIG_SERVER_KEY, ""),
            client_version=config_section.get(CONFIG_CLIENT_VERSION_KEY, ""),
            restpp_port=config_section.get(CONFIG_RESTPP_PORT, DEFAULT_RESTPP_PORT).__str__(),
            gs_port=config_section.get(CONFIG_GS_PORT, DEFAULT_GS_PORT).__str__(),
            use_auth=use_auth,
            username=config_section.get(CREDENTIALS_USERNAME_KEY, ""),
            password=config_section.get(CREDENTIALS_PASSWORD_KEY, ""),
            secrets=secrets
        )


def __read_config_files__(raise_on_nonexistent: bool = False) -> Dict[str, TgcliConfiguration]:
    """Retrieve all configurations from the config files"""
    if not (CONFIG_FILEPATH.exists() and CREDENTIALS_FILEPATH.exists()):
        if raise_on_nonexistent:
            raise TgcliConfigurationError(
                message="No valid configuration files exist.")
        else:
            return {}
    config = configparser.ConfigParser()
    config.optionxform = str  # Case sensitive
    config.read([CONFIG_FILEPATH, CREDENTIALS_FILEPATH])
    cli_configs: Dict[str, TgcliConfiguration] = {}
    for config_name in config.sections():
        cli_configs[config_name] = TgcliConfiguration.from_config_parser(config_name, config[config_name])
    return cli_configs


def save_configs(configs: Dict[str, TgcliConfiguration]):
    """Save the entire dictionary of configurations to files at $HOME/.tgcli/

    - .tgcli/config stores non-sensitive information
    - .tgcli/credentials stores sensitive information (username, password, and secrets)
    """
    combined_config = configparser.ConfigParser()
    combined_config.optionxform = str  # Case sensitive
    combined_credentials = configparser.ConfigParser()
    combined_credentials.optionxform = str  # Case sensitive
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
    """Retrieve all the configurations saved to config and credentials files in $HOME/.tgcli/"""
    return __read_config_files__(raise_on_nonexistent=raise_on_nonexistent)


def upsert_config(config: TgcliConfiguration):
    """Insert or overwrite configurations with the given config"""
    configs = __read_config_files__()
    configs[config.name] = config
    save_configs(configs)
