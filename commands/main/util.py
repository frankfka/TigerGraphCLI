from typing import Optional

from pyTigerGraph.pyTigerGraph import TigerGraphException

from tigergraph.common import get_tg_connection
from util import cli
from util.tgcli_config import get_configs


def get_initialized_tg_connection(config_name: str, graph_name: Optional[str] = None, require_graph: bool = False):
    """
    A wrapper to retrieve a working TigerGraph connection using CLI inputs
    """
    if require_graph and not graph_name:
        cli.terminate(1, "A graph name is required for this command.", is_err=True)
    config = get_configs().get(config_name, None)
    if not config:
        cli.terminate(1, "Invalid configuration. Please provide a valid configuration name.", is_err=True)
    return get_tg_connection(config, graph_name)
