# Usage - TigerGraphCLI (CLI)

CLI for interacting with TigerGraph.

**Usage**:

```console
$ tgcli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `config`: Manage TigerGraph configurations for tgcli.
* `delete`: Delete data from your TigerGraph server.
* `get`: Get resources from your TigerGraph server.
* `gsql`: Run GSQL commands against a TigerGraph...
* `load`: Load data into your TigerGraph server.
* `reinit-dependencies`: Force download dependencies and generate a...
* `version`

## `tgcli config`

Manage TigerGraph configurations for tgcli.

**Usage**:

```console
$ tgcli config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Adds a TgcliConfiguration interactively
* `delete`: Deletes a configuration when given the config...
* `describe`: Describe a configuration when given the...
* `list`: List all the TgcliConfigurations currently...

### `tgcli config add`

Adds a TgcliConfiguration interactively

**Usage**:

```console
$ tgcli config add [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `tgcli config delete`

Deletes a configuration when given the config name

**Usage**:

```console
$ tgcli config delete [OPTIONS] [NAME]
```

**Options**:

* `[NAME]`: The name of the configuration to use with the command.
* `--help`: Show this message and exit.

### `tgcli config describe`

Describe a configuration when given the config name

This will print all the parameters of the configuration to console,

**Usage**:

```console
$ tgcli config describe [OPTIONS] [CONFIG_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `--show-sensitive`: Show password and secret in output if specified.  [default: False]
* `--help`: Show this message and exit.

### `tgcli config list`

List all the TgcliConfigurations currently available

Using this command will print out all the configuration names and their respective servers

**Usage**:

```console
$ tgcli config list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `tgcli delete`

Delete data from your TigerGraph server.

**Usage**:

```console
$ tgcli delete [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `edges`: Delete a set of edges.
* `vertices`: Delete a set of vertices, either by ID or by...

### `tgcli delete edges`

Delete a set of edges.

**Usage**:

```console
$ tgcli delete edges [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--from-type TEXT`: Type of the source vertex.  [required]
* `--from-id TEXT`: ID of the source vertex.  [required]
* `--to-id TEXT`: ID of the target vertex
* `--to-type TEXT`: Type of the target vertex. Required if '--to-id' is specified.
* `--edge-type TEXT`: Type of the edge. Required if '--to-id' and '--to-type' are specified.
* `--where TEXT`: A condition to match for returned edges, multiple can be specified by using the flag multiple times. Multiple conditions are joined with AND. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter. For string conditions, the literal can be escaped like so: '--where=gender=\"male\"'. Alternatively, string escapes can be replaced by the URL-encoded string '%22'.  [default: ]
* `--sort TEXT`: Attribute name to sort results by, multiple can be specified by using the flag multiple times. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort.  [default: ]
* `--limit INTEGER`: Maximum number of results to retrieve.  [default: 10]
* `--timeout INTEGER`: Timeout in seconds.  [default: 60]
* `--help`: Show this message and exit.

### `tgcli delete vertices`

Delete a set of vertices, either by ID or by a query

**Usage**:

```console
$ tgcli delete vertices [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--type TEXT`: Type of the vertex.  [required]
* `--id TEXT`: ID of the vertex to retrieve, multiple can be specified by using the flag multiple times. If this is specified, other query parameters are ignored.  [default: ]
* `--where TEXT`: A condition to match for returned vertices, multiple can be specified by using the flag multiple times. Multiple conditions are joined with AND. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter . For string conditions, the literal can be escaped like so: '--where=gender=\"male\"'. Alternatively, string escapes can be replaced by the URL-encoded string '%22'.  [default: ]
* `--sort TEXT`: Attribute name to sort results by, multiple can be specified by using the flag multiple times. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort.  [default: ]
* `--permanent`: If true, the deleted ID's cannot be reinserted without either dropping the graph or clearing the graph store.  [default: False]
* `--limit INTEGER`: Maximum number of results to retrieve.  [default: 10]
* `--timeout INTEGER`: Timeout in seconds.  [default: 60]
* `--help`: Show this message and exit.

## `tgcli get`

Get resources from your TigerGraph server.

**Usage**:

```console
$ tgcli get [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `edges`: Get a set of edges
* `schema`: Retrieve the schema for the configuration
* `types`: Get a set of types, either vertices or edges.
* `vertices`: Get a set of vertices, either by ID or by...

### `tgcli get edges`

Get a set of edges

**Usage**:

```console
$ tgcli get edges [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--from-type TEXT`: Type of the source vertex.  [required]
* `--from-id TEXT`: ID of the source vertex.  [required]
* `--to-id TEXT`: ID of the target vertex
* `--to-type TEXT`: Type of the target vertex. Required if '--to-id' is specified.
* `--edge-type TEXT`: Type of the edge. Required if '--to-id' and '--to-type' are specified.
* `--attr TEXT`: Attributes to return for each edge, multiple can be specified by using the flag multiple times. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#select.  [default: ]
* `--where TEXT`: A condition to match for returned edges, multiple can be specified by using the flag multiple times. Multiple conditions are joined with AND. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter. For string conditions, the literal can be escaped like so: '--where=gender=\"male\"'. Alternatively, string escapes can be replaced by the URL-encoded string '%22'.  [default: ]
* `--sort TEXT`: Attribute name to sort results by, multiple can be specified by using the flag multiple times. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort.  [default: ]
* `--limit INTEGER`: Maximum number of results to retrieve.  [default: 10]
* `--timeout INTEGER`: Timeout in seconds.  [default: 60]
* `--help`: Show this message and exit.

### `tgcli get schema`

Retrieve the schema for the configuration

**Usage**:

```console
$ tgcli get schema [OPTIONS] CONFIG_NAME GRAPH_NAME
```

**Options**:

* `CONFIG_NAME`: [required]
* `GRAPH_NAME`: [required]
* `--help`: Show this message and exit.

### `tgcli get types`

Get a set of types, either vertices or edges. If no optioans are given, all types are returned.

**Usage**:

```console
$ tgcli get types [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--vertex TEXT`: Vertex type name to query. Specify * to query all.  [default: ]
* `--edge TEXT`: Vertex type name to query. Specify * to query all.  [default: ]
* `--help`: Show this message and exit.

### `tgcli get vertices`

Get a set of vertices, either by ID or by query

**Usage**:

```console
$ tgcli get vertices [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--type TEXT`: Type of the vertex.  [required]
* `--id TEXT`: ID of the vertex to retrieve, multiple can be specified by using the flag multiple times. If this is specified, other query parameters are ignored.  [default: ]
* `--attr TEXT`: Attributes to return for each vertex, multiple can be specified by using the flag multiple times. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#select .  [default: ]
* `--where TEXT`: A condition to match for returned vertices, multiple can be specified by using the flag multiple times. Multiple conditions are joined with AND. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter . For string conditions, the literal can be escaped like so: '--where=gender=\"male\"'. Alternatively, string escapes can be replaced by the URL-encoded string '%22'.  [default: ]
* `--sort TEXT`: Attribute name to sort results by, multiple can be specified by using the flag multiple times. See https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort.  [default: ]
* `--limit INTEGER`: Maximum number of results to retrieve.  [default: 10]
* `--timeout INTEGER`: Timeout in seconds.  [default: 60]
* `--help`: Show this message and exit.

## `tgcli gsql`

Run GSQL commands against a TigerGraph server.

**Usage**:

```console
$ tgcli gsql [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `run`: Run a GSQL query against a configuration...

### `tgcli gsql run`

Run a GSQL query against a configuration through an inline command, file, or interactive editor

**Usage**:

```console
$ tgcli gsql run [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--command TEXT`: Inline GSQL command
* `--file FILE`: Filepath to load a GSQL command from.
* `--editor`: Launch an interactive editor to load the GSQL command  [default: False]
* `--help`: Show this message and exit.

## `tgcli load`

Load data into your TigerGraph server.

**Usage**:

```console
$ tgcli load [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `edges`: Loads a set of edges from a given datasource.
* `vertices`: Loads a set of vertices from a given...

### `tgcli load edges`

Loads a set of edges from a given datasource.

**Usage**:

```console
$ tgcli load edges [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--source-type TEXT`: Type name of the source vertex  [required]
* `--source-id TEXT`: Column name for the source vertex ID  [required]
* `--target-type TEXT`: Type name of the target vertex  [required]
* `--target-id TEXT`: Column name for the target vertex ID  [required]
* `--edge-type TEXT`: Type name of the edge  [required]
* `--edge-attr TEXT`: Column name of an edge attribute, multiple can be specified by using the flag multiple times. If none are provided, all columns except for the source and target vertex ID columns are used.  [default: ]
* `--csv FILE`: CSV filepath to load vertices from.
* `--pickle FILE`: Pickle filepath to load vertices from.
* `--json FILE`: JSON filepath to load vertices from.
* `--help`: Show this message and exit.

### `tgcli load vertices`

Loads a set of vertices from a given datasource.

**Usage**:

```console
$ tgcli load vertices [OPTIONS] [CONFIG_NAME] [GRAPH_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `[GRAPH_NAME]`: The name of the graph to us with the command.
* `--type TEXT`: Vertex type to map data to.  [required]
* `--id TEXT`: Column name to set as the ID of the vertex  [required]
* `--attr TEXT`: Column name of an vertex attribute, multiple can be specified by using the flag multiple times. If no values are provided, all columns will be used.  [default: ]
* `--csv FILE`: CSV filepath to load vertices from.
* `--pickle FILE`: Pickle filepath to load vertices from.
* `--json FILE`: JSON filepath to load vertices from.
* `--help`: Show this message and exit.

## `tgcli reinit-dependencies`

Force download dependencies and generate a new secret for the configuration

**Usage**:

```console
$ tgcli reinit-dependencies [OPTIONS] [CONFIG_NAME]
```

**Options**:

* `[CONFIG_NAME]`: The name of the configuration to use with the command.
* `--help`: Show this message and exit.

## `tgcli version`

**Usage**:

```console
$ tgcli version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
