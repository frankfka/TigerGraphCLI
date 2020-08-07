"""
Functions to initialize dependencies for TigerGraph
"""
from pathlib import Path
import shutil
from typing import Optional

from pyTigerGraph import TigerGraphConnection

from util.io import APP_DIR
from util.tgcli_config import TgcliConfiguration, upsert_config

CERT_FILENAME = "cert.txt"


def get_dependencies_folder(config: TgcliConfiguration) -> Path:
    return APP_DIR / config.name


def get_jar_folder(config: TgcliConfiguration) -> Path:
    return get_dependencies_folder(config)


def get_cert_filepath(config: TgcliConfiguration) -> Path:
    return get_dependencies_folder(config) / CERT_FILENAME


def get_jar_filepath(config: TgcliConfiguration) -> Path:
    return get_jar_folder(config) / "gsql_client.jar"  # This is dependent on pyTigerGraph (hardcoded filename)


def init_dependencies(config: TgcliConfiguration,
                      conn: Optional[TigerGraphConnection],
                      clean_init: bool = False):
    """
    Initialize dependencies by downloading the TigerGraph jar and the cert, if needed
    - if clean_init is specified, dependencies will be redownloaded
    """
    jar_fp = get_jar_filepath(config)
    jar_folder = get_jar_folder(config)
    cert_fp = get_cert_filepath(config)
    if jar_fp.exists() and (config.use_auth and cert_fp.exists()) and not clean_init:
        # Already initialized
        return
    if not conn:
        conn = __get_tg_connection___(config)
    conn.initGsql(jarLocation=jar_folder, certLocation=cert_fp)  # Use pyTigerGraph to download dependencies


def delete_dependencies(config: TgcliConfiguration):
    shutil.rmtree(get_dependencies_folder(config), ignore_errors=True)


def __get_tg_connection___(config: TgcliConfiguration, graph_name: Optional[str] = None) -> TigerGraphConnection:
    """
    Base method to get a connection, just a lightweight wrapper around pyTigerGraph
    """
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
    """
    Initialize a TigerGraph connection when given a configuration and an optional graph name
    - if clean_init is specified, secret will be force updated
    """
    conn = __get_tg_connection___(config, graph_name)
    init_dependencies(config, conn, clean_init=clean_init)  # Manually download dependencies
    conn.gsqlInitiated = True
    conn.downloadCert = False
    conn.downloadJar = False
    conn.jarLocation = get_jar_folder(config).expanduser().__str__()
    conn.certLocation = get_cert_filepath(config).expanduser().__str__()
    conn.initGsql(conn.jarLocation, conn.certLocation)  # Still call init for other dependencies (self.url)
    if config.use_auth:
        # TODO: Consider catching TigerGraph exception
        secret = config.secret
        if not secret or clean_init:
            print("Creating new secret from credentials and saving to configuration.")
            secret = conn.createSecret()
            if not secret:
                raise ValueError("Could not create a secret for the connection.")
            # Also save the new config
            config.secret = secret
            upsert_config(config)
        # Finally, get the token
        conn.getToken(secret=secret)
    return conn
