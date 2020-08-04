from typing import List

import typer

get_app = typer.Typer()


@get_app.command("vertices")
def get_vertices(
        # Basic config
        config_name: str,
        graph_name: str,
        # Required items
        vertex_type: str = typer.Option(..., "--type", help="Type of the vertex."),
        # ID's take precedence if given
        vertex_ids: List[str] = typer.Option(
            [], "--id",
            help="ID of the vertex to retrieve, multiple can be specified by using the flag multiple times."
        )
):
    # TODO
    pass
