from typing import List

import typer

from tgcli.commands.etc.help_text import GRAPH_ARG_HELP, CONFIG_ARG_HELP
from tgcli.commands.util import get_initialized_tg_connection, resolve_multiple_args, preprocess_list_query
from tgcli.util import cli

get_app = typer.Typer(help="Get resources from your TigerGraph server.")


@get_app.command("vertices")
def get_vertices(
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
        attributes: List[str] = typer.Option(
            [], '--attr',
            help="Attributes to return for each vertex, multiple can be specified by using the flag multiple times. "
                 "See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#select ."
        ),
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
        limit: int = typer.Option(10, '--limit', help="Maximum number of results to retrieve."),
        timeout: int = typer.Option(60, '--timeout', help="Timeout in seconds.")
):
    """Get a set of vertices, either by ID or by query"""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    if vertex_ids:
        # Given ID's give precedence
        output = conn.getVerticesById(vertex_type, resolve_multiple_args(vertex_ids))
    else:
        output = conn.getVertices(
            vertex_type,
            select=preprocess_list_query(attributes),
            where=preprocess_list_query(where),
            sort=preprocess_list_query(sort_by_attrs),
            limit=limit,
            timeout=timeout
        )
    cli.print_to_console(output)


@get_app.command("edges")
def get_edges(
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
        attributes: List[str] = typer.Option(
            [], '--attr',
            help="Attributes to return for each edge, multiple can be specified by using the flag multiple times. "
                 "See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#select."
        ),
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
    """Get a set of edges"""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    if target_vertex_id and (not target_vertex_type or not edge_type):
        cli.terminate(message="Target vertex ID is specified but target vertex type or edge type isn't.", is_err=True)
    output = conn.getEdges(
        sourceVertexType=source_vertex_type,
        sourceVertexId=source_vertex_id,
        targetVertexType=target_vertex_type,
        targetVertexId=target_vertex_id,
        edgeType=edge_type,
        select=preprocess_list_query(attributes),
        where=preprocess_list_query(where),
        sort=preprocess_list_query(sort_by_attrs),
        limit=limit,
        timeout=timeout
    )
    cli.print_to_console(output)


@get_app.command("types")
def get_type_info(
        # Basic config
        config_name: str = typer.Argument(None, help=CONFIG_ARG_HELP),
        graph_name: str = typer.Argument(None, help=GRAPH_ARG_HELP),
        # Types to query
        vertex_type_names: List[str] = typer.Option(
            [], "--vertex", help="Vertex type name to query. Specify * to query all."
        ),
        edge_type_names: List[str] = typer.Option(
            [], "--edge", help="Vertex type name to query. Specify * to query all."
        )
):
    """Get a set of types, either vertices or edges. If no optioans are given, all types are returned."""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name, require_graph=True)
    results = {}
    query_all = (not vertex_type_names) and (not edge_type_names)
    if vertex_type_names or query_all:
        vertex_types = resolve_multiple_args(vertex_type_names)
        if query_all:
            vertex_types = "*"
        results.update(conn.getVertexStats(vertex_types))
    if edge_type_names or query_all:
        edge_types = resolve_multiple_args(edge_type_names)
        if query_all:
            edge_types = "*"
        results.update(conn.getEdgeStats(edge_types))
    cli.print_to_console(results)


@get_app.command("schema")
def get_schema(config_name: str, graph_name: str):
    """Retrieve the schema for the configuration"""
    conn = get_initialized_tg_connection(config_name=config_name, graph_name=graph_name)
    output = conn.getSchema()
    cli.print_to_console(output)
