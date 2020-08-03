from pathlib import Path

import typer
import pandas as pd

from commands.main.util import get_initialized_tg_connection
from util import cli

load_app = typer.Typer()


@load_app.command(name="vertices")
def load_vertices(
        config_name: str,
        graph_name: str,
        vertex_type: str = typer.Option(..., "--type", help="Vertex type to map data to.", prompt="Vertex type"),
        vertex_id_col: str = typer.Option(..., "--id", help="Column name to set as the ID of the vertex",
                                          prompt="Column name for ID"),
        csv_filepath: Path = typer.Option(
            None, "--csv", help="CSV filepath to load vertices from.",
            exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
        )
):
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    num_upserted: int = 0
    if csv_filepath:
        num_upserted = conn.upsertVertexDataframe(
            df=pd.read_csv(csv_filepath),
            vertexType=vertex_type,
            v_id=vertex_id_col
        )
    # TODO: json, pickle
    else:
        cli.terminate(message="No vertices loaded. Please specify a data source.")
    cli.print_to_console(f"Vertex load success. {num_upserted} vertices added.")

# TODO: edges