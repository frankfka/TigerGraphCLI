# TigerGraphCLI (tgcli)
TigerGraphCLI is a command-line utility for interacting with [TigerGraph](https://www.tigergraph.com/) servers. It's
built on top of [pyTigerGraph](https://github.com/pyTigerGraph/pyTigerGraph).

This project is still under active development. If you find a bug or have a feature request, feel free to create a Github issue.

## Installation
tgcli works best with Python 3.7+, but should work with any Python3 distribution. Installation is simple:
`pip3 install tigergraphcli`.

Verify your installation by running `tgcli version`

Once installed, get started by creating a configuration, which holds all the config and credentials needed to
connect to a TigerGraph server. You can do this by running `tgcli config add`. This will guide you through creating
a tgcli configuration.

## Usage

There are 5 main operations that tgcli supports:

1. `tgcli config`: Manages TigerGraph server configurations. Configurations are stored in a folder named `.tgcli`
under the home directory (ex. `~/.tgcli`)
2. `tgcli gsql`: Runs a GSQL command against a TigerGraph server
3. `tgcli load`: Loads vertices/edges to a TigerGraph server
4. `tgcli get`: Retrieves data from a TigerGraph server
5. `tgcli delete`: Delete data from a TigerGraph server.

See [usage](./docs/USAGE.md) for detailed documentation.