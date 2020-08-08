from typing import Optional, Tuple, Any, List

from tgcli.tigergraph.common import get_tg_connection
from tgcli.util import cli
from tgcli.util.tgcli_config import get_configs


def get_initialized_tg_connection(config_name: str, graph_name: Optional[str] = None,
                                  require_graph: bool = False, clean_init: bool = False):
    """A wrapper to retrieve a working TigerGraph connection using CLI inputs"""
    if require_graph and not graph_name:
        cli.terminate(1, "A graph name is required for this command.", is_err=True)
    config = get_configs().get(config_name, None)
    if not config:
        cli.terminate(1, "Invalid configuration. Please provide a valid configuration name.", is_err=True)
    return get_tg_connection(config, graph_name, clean_init=clean_init)


def resolve_multiple_args(args: Tuple[Any]) -> List[Any]:
    """A temporary workaround to address: https://github.com/tiangolo/typer/issues/127"""
    return list(args)


def preprocess_list_query(queries: List[str]):
    """Preprocesses a list of provided conditions into what the REST api expects (comma separated string)"""
    # Note: could use resolve_multiple_args but the same comprehension works for tuples
    return ",".join([q.strip() for q in queries])
