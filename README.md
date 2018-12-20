# Black Hat EU 2018 - Don't Eat Spaghetti with a Spoon - An Analysis of the Practical Value of Threat Intelligence #

#### Presented by: Charl van der Walt and Sid Pillarisetty 

The data contained in this project was used by the authors in preperation of their BH EU 2018 talk. The data has been scrubed to ensure a level of anonimity, yet it contains the same reference capability to review and potentially repeat the research independently.

The data provided as a Postgres 10 database dump. This is a text dump that is GZip'ed. It can befound in the _bheu_data_ direcotry.

USers of the data can opt for two potential avenues when interacting with the data:

1. Restore the data in an existing Postgres 10 compatible database server. This will require some manual processing.
2. Use the supplied dockerized solution if you are so inclined.

We used a dedicated Amazon Postgres RDS instance with 1TB of storage running on SSDs. This provided a responsive platform given the type of queries we were running.  If you opt for running Postgres in Docker we suggest that you are patient and have sufficient disk space (500GB) available. RAM might be an issue so ensure that you have about 8GB RAM spare.

## Restoring data to a Postgres database server

Clone this GitHub project. Locate the file in the _bheu_data_ folder named _bheu-dump-scrubbed_event_data_import-20181130_00.sql.gz_.

On a Linux host use the following command:

    gunzip -c bheu-dump-scrubbed_event_data_import-20181220_00.sql.gz | pqsl -h localhost -U postgres -W -d postgres

This assumes the following:

* That the gzip file is in the current working directory.
* The Postgres 10 database server is running locally, hence localhost.
* The data in the GZip archive expects the postgres user and role.
* The data will be imported into the postgres database.
* That the username is postgres and there is a password.

To import this dump into Postgres under another database name and/or user role is not covered in this section and requires experience with Postgres/SQL.

## Using the Dockerized option

Clone the GitHub project. You need to run Docker version 17 or newer and it needs to have docker-compose support. Also, you will need the ability to allow Docker to mountp host directories in the Postgres Docker image.

Run the following in the cloned project directory:

    docker-compose up

This will download the Postgres 10 image and start the container. Part of the start up process will involve importing the data used in the research. The docker-compose.yml file maps the _bheu_data_ directory to the internal directory named _docker-entrypoint-initdb.d_ located within the Postgres Docker image. The Postgres image is set to automatically import any file ending with sql.gz.

You should see the following once the data has been imported:

![Postgres import](https://raw.githubusercontent.com/SecureDataLabs/BlackHat-EU-2018/master/docker_data_import.png)

A table called _event_data_import_ will be present in the postgres database.
## Preparing the data sets

We now need to prepare the various data sets before the analysis can start. This will require the creation of 15 tables that houses the respective data sets given time periods and correleations.

This can be done manually or through the Python scripts that we supplied.

1. Doing this manually will require you to use an interface that can execute the SQL instructions. User interfaces such as psql, pgAdmin or DBeaver are example that allow you to manually execute the relevant SQL.
    * See the file labelled _prepared_sql.txt_ in the root of the project.
    * This will contain the SQL to create the tables, run the import statements and create the indexes.
    * The table create SQL must be executed first, followed by the inesert statements. The indexes can be created last. This is to improve insert speed.
2. Use the supplied Python script to do the same programmatically.
    * Python 3.5 is recommended.
    * To get the correct requirements, run the following command in the event_importer directory:
        * pip install -r requirements.txt
    * To import the code run the following in the event_importer directory:
        * python prepare_schema.py -H localhost -p 35432 -D postgres -U postgres -P ""
    * Note that the Docker container maps the Postgres port 5432 as 35432.

*NOTE:* The import statements can take several minutes if not hours to run depending on the resources available to the Postgres database. We used an Amazon Postgres RDS instance with 1TB of storage running on SSDs. This dramatically improved the speed.

## Omitted data

Inlcuded in this project is the Python code that we used to import data from the raw sources. Those datasets were not included because of the senstive nature of the data. We did include the Python code that we used to import these data with.

The _import.py_ Python script is the entry point for this. It is used to import the Modern Honey Net data, repeat offenders, roguelist, threat intel lists, etc.

The _scrubdata.py_ Python script was used to anonymise the source and destination IP data that we included in this project.