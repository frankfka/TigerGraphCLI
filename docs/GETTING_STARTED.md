# Getting Started with TGCLI

In this walkthrough, we will be using the [GSQL 101](https://docs-beta.tigergraph.com/start/gsql-101) starter kit available 
on [TigerGraph Cloud](https://tgcloud.io) to demonstrate some of the functionality that TGCLI provides.

## 1 Setting Up

Free cloud instances are available on [TigerGraph Cloud](https://tgcloud.io/). To get started, register an account
and login to the console.

Next, provision a free database instance, selecting the **GSQL 101** starter kit. Take note of the following:

- Domain - e.g. xyz.i.tgcloud.io
- Username - tigergraph by default
- Password - chosen during the setup process

Finally, make sure that you have an up-to-date version of TGCLI by following the [installation instructions](https://github.com/frankfka/TigerGraphCLI#installation)

## 2 Adding a Server Configuration

We first want to configure TGCLI with the server settings for the new cloud instance. You can add a configuration by using:

```
tgcli config add
```

This command will launch an interactive session to create the new configuration. Enter your domain, prefixed with `https://`,
as well as the username and password for the instance. An example would be:

```
Server Address (ex. https://xyz.i.tgcloud.io): https://xyz.i.tgcloud.io
Client Version (3.0.0, 2.6.0, 2.5.2, 2.5.0, 2.4.1, 2.4.0, 2.3.2): 2.6.0
REST++ Port [9000]: 
GS Port [14240]: 
Use Auth (This is usually true) [Y/n]: Y
Username [tigergraph]: 
Password [tigergraph]: YOUR_PASSWORD
Name (Alphanumeric & Underscore Allowed): gsql101
Configuration gsql101 added for server https://xyz.i.tgcloud.io
```

You can check that the new configuration is valid by running `tgcli gsql run gsql101 --command ls`:

```
tgcli gsql run gsql101 --command ls
/usr/bin/java
Downloading gsql client Jar
/usr/bin/openssl
Downloading SSL Certificate
/usr/bin/java
========================
Trying version: v2_6_0
Connecting to xyz.i.tgcloud.io:14240
If there is any relative path, it is relative to tigergraph/dev/gdk/gsql
---- Global vertices, edges, and all graphs
Vertex Types: 
  - VERTEX person(PRIMARY_ID name STRING, name STRING, age INT, gender STRING, state STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE", PRIMARY_ID_AS_ATTRIBUTE="false"
Edge Types: 
  - UNDIRECTED EDGE friendship(FROM person, TO person, connect_day DATETIME)

Graphs: 
  - Graph social(person:v, friendship:e)
Jobs: 


JSON API version: v2
Syntax version: v1
```

Notice that the first time a configuration is used, TGCLI will automatically download the required client jar and certs needed
to communicate with the server.

## 3 Defining a Schema

