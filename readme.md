# International Space Station Data Engineering Live Streaming Project

This project aims to create a robust data engineering pipeline using technologies such as Apache Airflow, Apache Kafka, Apache Zookeeper, Apache Spark, Cassandra, Python, and Docker.

## Overview

The project involves fetching real-time data from the ISS API, streaming it to Kafka, and then using Spark to insert this data into Cassandra. Additionally, a mechanism will be implemented to receive an email notification when the ISS is overhead at the current location during nighttime, allowing for the observation of the fastest-moving object in the sky.

## Dashboard

A dashboard will be created to visualize the ISS's longitude and latitude on a world map, with the ability to filter by date.

[Link to final dashboard](https://isspydash.prabshhs.in)

## Architecture Flowchart

![FLowchart](ISS_system_Architecture.png)

## Docker Containers and Configuration

To set up the data pipeline, an environment hosting all the required services will be created. One approach is to create a Docker bridge network and run containers for all these services within this network.

Create Docker network:

```bash
docker network create --driver bridge ISS_proj
```

### Airflow container

[Link to Docker compose file](Containers/Airflow/docker-compose.yml)

In this docker compose file there are total 3 containers required for the working of Apache Airflow

1. Airflow Webserver- Provides user interface for Airflow. It allow users to interact with DAGs etc. `DAGs(Direct Acyclic Graphs) is collection of tasks that you want to run on a schedule represented as a Python script where each task is an instance of an operator` [Dag location](Containers/Airflow/dags)
2. Scheduler- Crucial component responsible for scheduling the execution of DAGs
3. PostgreSQL- Store the Metadata of Airflow

`FYI:` [entrypoint.sh](Containers/Airflow/script/entrypoint.sh) `This file will run first when docker container is initiated for run` note - if error comes and entrypoint.sh is not executable then use `chmod +x entrypoint.sh`

[requirements.txt](Containers/Airflow/requirements.txt) `This file contains list of all packages which is required inside the container, if new package is required install using this`


#### Additional configuration for sending mail

In python for sending mail via SMTP it required email and its password(or API key), I am passing the email and password through the environment variable

Add following in airflow webserver and scheduler docker-compose.yml file -

```yml
services:
  webserver:
    environment:
      - GMAIL_EMAIL=your_email@gmail.com
      - GMAIL_PASSWORD=your_password
```


```bash
docker compose -f "Airflow/docker-compose.yml" up -d
# go to http://192.168.1.111:8536/
```

### Kafka container

[Link to docker compose file](Containers/Kafka/docker-compose.yml)

There are 4 containers inside this docker compose:

1. Zookeeper: Manage and coordinate brokers in the kafka cluster
2. Broker: are the kafka servers, they store and manage message logs
3. Schema Registry: Optional component that is used when working with Avro serialization in Kafka, this ensures that producer and consumers can exchange messages with compatible schemas
4. Control Center: it is a management and monitoring tool for Kafka cluster

### Spark Cluster containers

Spark cluster has Master and Worker architecture, 

1. Master Node: it coordinates the execution of spark applications and manages the cluster resources
2. Worker Node: this perform the actual data processing tasks


