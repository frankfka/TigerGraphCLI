"""
Functions to initialize dependencies for TigerGraph
"""
from pathlib import Path
import shutil
from typing import Optional

from pyTigerGraph import TigerGraphConnection

from util.io import APP_DIR
from util.tgcli_config import TgcliConfiguration


CERT_FILENAME = "cert.txt"


def get_dependencies_folder(config: TgcliConfiguration) -> Path:
    return APP_DIR / config.name


def get_jar_folder(config: TgcliConfiguration) -> Path:
    return get_dependencies_folder(config)


def get_cert_filepath(config: TgcliConfiguration) -> Path:
    return get_dependencies_folder(config) / CERT_FILENAME


def get_jar_filepath(config: TgcliConfiguration) -> Path:
    return get_jar_folder(config) / "gsql_client.jar"  # TODO: This is dependent on pyTigerGraph (hardcoded filename)


def init_dependencies(config: TgcliConfiguration, conn: Optional[TigerGraphConnection]):
    """
    Initialize dependencies by downloading the TigerGraph jar and the cert, if needed
    """
    jar_fp = get_jar_filepath(config)
    jar_folder = get_jar_folder(config)
    cert_fp = get_cert_filepath(config)
    if jar_fp.exists() and cert_fp.exists():
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
        restppPort='9000',
        gsPort='14240',
        apiToken=''
    )


def get_tg_connection(config: TgcliConfiguration, graph_name: Optional[str] = None) -> TigerGraphConnection:
    """
    Initialize a TigerGraph connection when given a configuration and an optional graph name
    """
    conn = __get_tg_connection___(config, graph_name)
    init_dependencies(config, conn)  # Manually download dependencies
    conn.gsqlInitiated = True
    conn.downloadCert = False
    conn.downloadJar = False
    conn.jarLocation = get_jar_folder(config).expanduser().__str__()
    conn.certLocation = get_cert_filepath(config).expanduser().__str__()
    conn.initGsql(conn.jarLocation, conn.certLocation)  # Still call init for other dependencies (self.url)
    return conn
