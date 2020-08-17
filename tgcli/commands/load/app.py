from pathlib import Path
from typing import List

import typer
import pandas as pd

from tgcli.commands.etc.help_text import CONFIG_ARG_HELP, GRAPH_ARG_HELP
from tgcli.commands.util import get_initialized_tg_connection
from tgcli.util import cli


def __get_df__(path: Path, filetype: str) -> pd.DataFrame:
    """Retrieves a pandas dataframe from a source"""
    if filetype is "csv":
        return pd.read_csv(path)
    elif filetype is "pickle":
        return pd.read_pickle(path)
    elif filetype is "json":
        return pd.read_json(path)


load_app = typer.Typer(help="Load data into your TigerGraph server.")


@load_app.command(name="vertices")
def load_vertices(
        # Basic config
        config_name: str = typer.Argument(None, help=CONFIG_ARG_HELP),
        graph_name: str = typer.Argument(None, help=GRAPH_ARG_HELP),
        # Required attributes
        vertex_type: str = typer.Option(..., "--type", help="Vertex type to map data to.", prompt="Vertex type"),
        vertex_id_col: str = typer.Option(..., "--id", help="Column name to set as the ID of the vertex",
                                          prompt="Column name for ID"),
        # No prompt here - must be provided via CLI (string split into chars because of typer processing)
        attrs: List[str] = typer.Option(
            [], "--attr",
            help="Column name of an vertex attribute, multiple can be specified by using the flag multiple times. "
                 "If no values are provided, all columns will be used.",
        ),
        # Data sources
        csv_filepath: Path = typer.Option(
            None, "--csv", help="CSV filepath to load vertices from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        ),
        pickle_filepath: Path = typer.Option(
            None, "--pickle", help="Pickle filepath to load vertices from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        ),
        json_filepath: Path = typer.Option(
            None, "--json", help="JSON filepath to load vertices from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        )
):
    """Loads a set of vertices from a given datasource."""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    num_upserted: int = 0
    vertex_attributes = None
    df = None
    if attrs:
        vertex_attributes = {val: val for val in attrs}
    if csv_filepath:
        df = __get_df__(csv_filepath, "csv")
    elif pickle_filepath:
        df = __get_df__(pickle_filepath, "pickle")
    elif json_filepath:
        df = __get_df__(json_filepath, "json")
    if df is not None:
        num_upserted = conn.upsertVertexDataframe(
            df=df,
            vertexType=vertex_type,
            v_id=vertex_id_col,
            attributes=vertex_attributes
        )
    else:
        cli.terminate(message="No vertices loaded. Please specify a data source.")
    cli.print_to_console(f"Vertex load success. {num_upserted} vertices added.")


@load_app.command(name="edges")
def load_edges(
        # Basic config
        config_name: str = typer.Argument(None, help=CONFIG_ARG_HELP),
        graph_name: str = typer.Argument(None, help=GRAPH_ARG_HELP),
        # Required items
        source_vertex_type: str = typer.Option(
            ..., "--source-type", help="Type name of the source vertex", prompt="Source vertex type"
        ),
        source_vertex_id_col: str = typer.Option(
            ..., "--source-id", help="Column name for the source vertex ID",
            prompt="Source vertex ID column name"
        ),
        target_vertex_type: str = typer.Option(
            ..., "--target-type", help="Type name of the target vertex", prompt="Target vertex type"
        ),
        target_vertex_id_col: str = typer.Option(
            ..., "--target-id", help="Column name for the target vertex ID",
            prompt="Target vertex ID column name"
        ),
        edge_type: str = typer.Option(
            ..., "--edge-type", help="Type name of the edge", prompt="Edge type"
        ),
        # No prompt here - must be provided via CLI (string split into chars because of typer processing)
        edge_attrs: List[str] = typer.Option(
            [], "--edge-attr",
            help="Column name of an edge attribute, multiple can be specified by using the flag multiple times. "
                 "If none are provided, all columns except for the source and target vertex ID columns are used.",
        ),
        # Data sources
        csv_filepath: Path = typer.Option(
            None, "--csv", help="CSV filepath to load vertices from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        ),
        pickle_filepath: Path = typer.Option(
            None, "--pickle", help="Pickle filepath to load vertices from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        ),
        json_filepath: Path = typer.Option(
            None, "--json", help="JSON filepath to load vertices from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        )
):
    """Loads a set of edges from a given datasource."""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    num_upserted: int = 0
    df = None
    ignore_cols = {source_vertex_id_col, target_vertex_id_col}
    if csv_filepath:
        df = __get_df__(csv_filepath, "csv")
    elif pickle_filepath:
        df = __get_df__(pickle_filepath, "pickle")
    elif json_filepath:
        df = __get_df__(json_filepath, "json")
    if df is not None:
        edge_attributes = {val: val for val in df.columns if val not in ignore_cols}
        if edge_attrs:
            edge_attributes = {val: val for val in edge_attrs}
        num_upserted = conn.upsertEdgesDataframe(
            df=df,
            sourceVertexType=source_vertex_type,
            targetVertexType=target_vertex_type,
            edgeType=edge_type,
            from_id=source_vertex_id_col,
            to_id=target_vertex_id_col,
            attributes=edge_attributes
        )
    else:
        cli.terminate(message="No edges loaded. Please specify a data source.")
    cli.print_to_console(f"Edge load success. {num_upserted} edges added.")
