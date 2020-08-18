"""Functions to initialize dependencies for TigerGraph, using pyTigerGraph"""
from pathlib import Path
import shutil
from typing import Optional

from pyTigerGraph import TigerGraphConnection

from tgcli.util.io import APP_DIR
from tgcli.util.tgcli_config import TgcliConfiguration, upsert_config

CERT_FILENAME = "cert.txt"


def get_dependencies_folder(config: TgcliConfiguration) -> Path:
    """Return dependencies folder, in .tgcli/CONFIG_NAME

    This stores the Java client and SSL cert
    """
    return APP_DIR / config.name


def get_jar_folder(config: TgcliConfiguration) -> Path:
    """Return the Java client folder, in .tgcli/CONFIG_NAME"""
    return get_dependencies_folder(config)


def get_cert_filepath(config: TgcliConfiguration) -> Path:
    """Return the SSL cert filepath, .tgcli/CONFIG_NAME/cert.txt"""
    return get_dependencies_folder(config) / CERT_FILENAME


def get_jar_filepath(config: TgcliConfiguration) -> Path:
    """Return the Java client filepath, .tgcli/CONFIG_NAME/gsql_client.jar"""
    return get_jar_folder(config) / "gsql_client.jar"  # This is dependent on pyTigerGraph (hardcoded filename)


def init_dependencies(config: TgcliConfiguration,
                      conn: Optional[TigerGraphConnection],
                      clean_init: bool = False):
    """Initialize dependencies by downloading the TigerGraph jar and the cert, if needed.

    If clean_init is specified, dependencies will be redownloaded. Otherwise if the cert and client already exist,
    no action is taken.
    """
    jar_fp = get_jar_filepath(config)
    jar_folder = get_jar_folder(config)
    cert_fp = get_cert_filepath(config)
    if jar_fp.exists() and (config.use_auth and cert_fp.exists()) and not clean_init:
        # Already initialized
        return
    if not conn:
        # Get a new connection if one wasn't given - the connection is used only to use pyTigerGraph to download deps
        conn = __get_tg_connection___(config)
    conn.initGsql(jarLocation=jar_folder, certLocation=cert_fp)  # Use pyTigerGraph to download dependencies


def delete_dependencies(config: TgcliConfiguration):
    """Delete the dependencies folder in tgcli/CONFIG_NAME"""
    shutil.rmtree(get_dependencies_folder(config), ignore_errors=True)


def __get_tg_connection___(config: TgcliConfiguration, graph_name: Optional[str] = None) -> TigerGraphConnection:
    """Retrieve a basic TigerGraph connection"""
    return TigerGraphConnection(
        host=config.server,
        username=config.username,
        password=config.password,
        clientVersion=config.client_version,
        graphname=graph_name or '',
        restppPort=config.restpp_port,
        gsPort=config.gs_port,
        apiToken='',
        useCert=config.use_auth
    )


def get_tg_connection(config: TgcliConfiguration,
                      graph_name: Optional[str] = None,
                      clean_init: bool = False) -> TigerGraphConnection:
    """Initialize a TigerGraph connection when given a configuration and an optional graph name

    - if clean_init is specified, dependencies will be force downloaded
    - if no graph_name is given, then operations will be run on the entire server (ex. for operations such as echo)
    """
    conn = __get_tg_connection___(config, graph_name)
    # Manually download dependencies and set flags in the underlying TigerGraphConnection
    # This gives more flexibility/control into what and where we download dependencies to
    init_dependencies(config, conn, clean_init=clean_init)
    conn.gsqlInitiated = True
    conn.downloadCert = False
    conn.downloadJar = False
    conn.jarLocation = get_jar_folder(config).expanduser().__str__()
    conn.certLocation = get_cert_filepath(config).expanduser().__str__()
    # Still call init for other dependencies (self.url) - but dependencies will not be downloaded
    conn.initGsql(conn.jarLocation, conn.certLocation)
    if config.use_auth and graph_name:
        # Get secret for the graph, if provided
        # TODO: Consider a class function for adding and retrieving secrets
        secret = config.secrets.get(graph_name, None)
        if not secret or clean_init:
            print(f"Creating new secret for graph {graph_name} and saving to configuration.")
            conn.graphname = graph_name
            secret = conn.createSecret()
            if not secret:
                raise ValueError(f"Could not create a secret for the connection to graph {graph_name}.")
            # Also save the new config
            config.secrets[graph_name] = secret
            upsert_config(config)
        # Finally, get the token
        conn.getToken(secret=secret)
    return conn
