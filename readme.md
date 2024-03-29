# International space station, end to end Data Engineering live streaming project

This project covers creation of robust data engineering pipeline, which uses various technologies like, Apache Airflow, Python, Apache Kafka, Apache Zookeeper, Apache Spark, Cassandra and Docker 

[Link to final dashboard](https://isspydash.prabshhs.in)

## Architecture Flowchart

![FLowchart](ISS_system_Architecture.png)

## Containers and their configrations 


### Add mail and password to envronment variable in airflow webserver and scheduler

<!-- this was a temprory solution, so added diretly to docker-compose file of airflow scheduler and webserver-->
<!-- docker exec -it airflow-scheduler-1 bash
docker exec -it airflow-webserver-1 bash
```bash

export GMAIL_EMAIL=your_email@gmail.com
export GMAIL_PASSWORD=your_password

env
```
 -->

add following in airflow webserve and scheduler docker-compose.yml file - 
```yml
services:
  webserver:
    environment:
      - GMAIL_EMAIL=your_email@gmail.com
      - GMAIL_PASSWORD=your_password
```

