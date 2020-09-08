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

The GSQL101 starter kit has a pre-defined schema when the database is provisioned. However, we'll walk through creating a schema
using TGCLI. To get started, we'll first clear the existing schema using `tgcli gsql run gsql101 --command "drop all"`. 
This usually takes a minute or so to complete.

Notice that we issue the command, `tgcli gsql run`, followed by the name of our new configuration, which we've configured to be `gsql101`.

We then issue an inline command using `--command`. 

Next, let's define the schema following the [GSQL101](https://docs-beta.tigergraph.com/start/gsql-101/define-a-schema) 
tutorial. The GSQL command itself is:

```
CREATE VERTEX person (
    PRIMARY_ID name STRING,
    name STRING, age INT,
    gender STRING, state STRING
)
```

To run a GSQL command using TGCLI, we can use the previous flag `--command` to issue an inline command. But for multiline
commands, it is easier to use the `--editor` flag to launch the interactive editor. Let's create the vertex by running:

`tgcli gsql run gsql101 --editor`

This launches the system editor. Go ahead and paste in the `CREATE VERTEX` command, then save and exit the editor. 
With `vim` as the default editor, for example, paste in the gsql command and type `:wq`.

Now that the vertex schema is created, we can go ahead and create the edge schema as well, using the gsql command:

```
CREATE UNDIRECTED EDGE friendship (FROM person, TO person, connect_day DATETIME)
```

Then, we can create the graph itself, using the gsql command:

```
CREATE GRAPH social (person, friendship)
```

To double check that everything was created properly, run `tgcli gsql run gsql101 --command ls`. You should see
that the output has the vertex type `person`, edge type `friendship`, and a graph named `social`. Nice job!

## 4 Loading Data

Now that we've defined a schema, we can load data to it using TGCLI. First, create the two `.csv` files from the
[GSQL101 dataset](https://docs.tigergraph.com/v/2.5/intro/gsql-101/get-set#GSQL101-DataSet). The tutorial will assume
that the relative paths of the files are `./person.csv` and `./friendship.csv`.

Let's load some vertices! Issue the command:

```
tgcli load vertices gsql101 social --type person --id name --csv ./person.csv
```

The output should be the following:

```
/usr/bin/java
Creating new secret for graph social and saving to configuration.
Vertex load success. 7 vertices added.
```

Notice that the first time we communicate with a given graph, a secret will be created. This is used to generate
API keys to talk to the remote GSQL server.

We can then proceed to load edges:

```
tgcli load edges gsql101 social \
    --source-type person --source-id person1 --target-type person --target-id person2 \
    --edge-type friendship --edge-attr connect_day \
    --csv ./friendship.csv
```

Once you run the command, you should see an error. This is because the edge attribute is called `connect_day`, but
the column in the CSV is actually called `date` - to fix this, rename the CSV column to `connect_day`. Rerun the command
and you should have loaded the correct edges.

We're all done with loading data!

## 5 Getting Data

Now that we have loaded some data, let's try retrieving data from our graph database. To get a list of vertices:

```
tgcli get vertices gsql101 social --type person
```

This will return a list of all the vertices. TGCLI also gives the option to return certain attributes or to order/filter
by a particular attribute. See [Usage Docs](https://github.com/frankfka/TigerGraphCLI/blob/master/docs/USAGE.md) for details.

We can also retrieve edges in a similar way, but running:

```
tgcli get edges gsql101 social --from-type person --from-id Nancy
```

The above command should return a list of edges that are outbound from the `person` vertex with ID `Nancy`.

## 6 Deleting Data

Lastly, we'll try deleting data using TGCLI. Let's try deleting the edges that originate from Nancy:

```
tgcli delete edges gsql101 social --from-type person --from-id Nancy
```

We see that we get `{'friendship': 2}` returned - which means that 2 edges have been deleted. Now that the edges are deleted,
we can try deleting the vertex with ID `Nancy` (sorry Nancy!):

```
tgcli delete vertices gsql101 social --type person --id Nancy
```

We see that the returned result is `1`, which indicates that one vertex was deleted.

## 7 Wrap Up

That was a basic overview of the functionality enabled by TGCLI. As you can see, using the CLI tool means that you won't need
to write code to perform basic actions. To view more in-depth documentation, see [Usage Docs](https://github.com/frankfka/TigerGraphCLI/blob/master/docs/USAGE.md).
