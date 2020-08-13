from typing import List

import typer

from tgcli.commands.etc.help_text import CONFIG_ARG_HELP, GRAPH_ARG_HELP
from tgcli.commands.util import get_initialized_tg_connection, preprocess_list_query, resolve_multiple_args
from tgcli.util import cli

delete_app = typer.Typer(help="Delete data from your TigerGraph server.")


@delete_app.command("vertices")
def delete_vertices(
        # Basic config
        config_name: str = typer.Argument(None, help=CONFIG_ARG_HELP),
        graph_name: str = typer.Argument(None, help=GRAPH_ARG_HELP),
        # Required items
        vertex_type: str = typer.Option(..., "--type", help="Type of the vertex."),
        # Query by ID's. If given, ID's take precedence over the generic query
        vertex_ids: List[str] = typer.Option(
            [], "--id",
            help="ID of the vertex to retrieve, multiple can be specified by using the flag multiple times. If "
                 "this is specified, other query parameters are ignored."
        ),
        # Generic query params
        where: List[str] = typer.Option(
            [], '--where',
            help="A condition to match for returned vertices, "
                 "multiple can be specified by using the flag multiple times. "
                 "Multiple conditions are joined with AND. "
                 "See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter . "
                 "For string conditions, the literal can be escaped like so: '--where=gender=\\\"male\\\"'. "
                 "Alternatively, string escapes can be replaced by the URL-encoded string '%22'."
        ),
        sort_by_attrs: List[str] = typer.Option(
            [], '--sort',
            help="Attribute name to sort results by, multiple can be specified by using the flag multiple times. "
                 "See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort."
        ),
        permanent: bool = typer.Option(
            False, '--permanent',
            help="If true, the deleted ID's cannot be reinserted without either "
                 "dropping the graph or clearing the graph store.")
        ,
        limit: int = typer.Option(10, '--limit', help="Maximum number of results to retrieve."),
        timeout: int = typer.Option(60, '--timeout', help="Timeout in seconds.")
):
    """Delete a set of vertices, either by ID or by a query"""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    if vertex_ids:
        # Given ID's give precedence
        output = conn.delVerticesById(
            vertex_type, resolve_multiple_args(vertex_ids), permanent=permanent, timeout=timeout
        )
    else:
        output = conn.delVertices(
            vertex_type,
            where=preprocess_list_query(where),
            sort=preprocess_list_query(sort_by_attrs),
            limit=limit,
            timeout=timeout,
            permanent=permanent
        )
    cli.print_to_console(output)


@delete_app.command("edges")
def delete_edges(
        # Basic config
        config_name: str = typer.Argument(None, help=CONFIG_ARG_HELP),
        graph_name: str = typer.Argument(None, help=GRAPH_ARG_HELP),
        # Required items
        source_vertex_type: str = typer.Option(..., "--from-type", help="Type of the source vertex."),
        source_vertex_id: str = typer.Option(..., "--from-id", help="ID of the source vertex."),
        # Filter by target
        target_vertex_id: str = typer.Option(None, "--to-id", help="ID of the target vertex"),
        target_vertex_type: str = typer.Option(
            None, "--to-type", help="Type of the target vertex. Required if '--to-id' is specified."
        ),
        edge_type: str = typer.Option(
            None, "--edge-type", help="Type of the edge. Required if '--to-id' and '--to-type' are specified."
        ),
        # Generic query params
        where: List[str] = typer.Option(
            [], '--where',
            help="A condition to match for returned edges, "
                 "multiple can be specified by using the flag multiple times. "
                 "Multiple conditions are joined with AND. "
                 "See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter. "
                 "For string conditions, the literal can be escaped like so: '--where=gender=\\\"male\\\"'. "
                 "Alternatively, string escapes can be replaced by the URL-encoded string '%22'."
        ),
        sort_by_attrs: List[str] = typer.Option(
            [], '--sort',
            help="Attribute name to sort results by, multiple can be specified by using the flag multiple times. "
                 "See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort."
        ),
        limit: int = typer.Option(10, '--limit', help="Maximum number of results to retrieve."),
        timeout: int = typer.Option(60, '--timeout', help="Timeout in seconds.")
):
    """Delete a set of edges."""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    if target_vertex_id and (not target_vertex_type or not edge_type):
        cli.terminate(message="Target vertex ID is specified but target vertex type or edge type isn't.", is_err=True)
    output = conn.delEdges(
        sourceVertexType=source_vertex_type,
        sourceVertexId=source_vertex_id,
        targetVertexType=target_vertex_type,
        targetVertexId=target_vertex_id,
        edgeType=edge_type,
        where=preprocess_list_query(where),
        sort=preprocess_list_query(sort_by_attrs),
        limit=limit,
        timeout=timeout
    )
    cli.print_to_console(output)
