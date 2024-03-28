docker network create --driver bridge ISS_proj


docker compose -f "Kafka/docker-compose.yml" up -d

# go to http://192.168.1.111:9021/

# going to take time
docker compose -f "Airflow/docker-compose.yml" up -d
# go to http://192.168.1.111:8536/


sudo docker compose -f "Spark/docker-compose.yml" up -d
# go to http://192.168.1.111:9537/

# --- testing -- 
docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/scripts/spark_test.py

docker exec -it spark-spark-master-1 bash -c 'cp /opt/bitnami/spark/scripts/data.csv /opt/bitnami/spark/data/data.csv'

docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/scripts/spark_test_csv.py


# kafka data to spark 
docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /opt/bitnami/spark/scripts/kafka_spark_stream.py



# Cassandra
docker compose -f "Cassandra/docker-compose.yml" up -d

docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042

```sql
DESCRIBE KEYSPACES;
USE system;
DESCRIBE TABLES;

CREATE KEYSPACE IF NOT EXISTS my_keyspace
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

# USE my_keyspace;

# CREATE TABLE IF NOT EXISTS my_table (
#     id UUID PRIMARY KEY,
#     name TEXT,
#     age INT
# );


# INSERT INTO my_table (id, name, age) VALUES (uuid(), 'Alice', 30);

```

# testing -- 
# see the ip address of cassandra in the netowrk
# docker network inspect ISS_proj


# Cassandra and spark conneciton test
docker exec -it spark-spark-master-1 bash

```bash
pyspark

# run cassandra_conneciton_test.py file line by line

```

docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 --packages com.datastax.spark:spark-cassandra-connector_2.12:3.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /opt/bitnami/spark/scripts/kafka_spark_cassandra_steam.py


# check if data is streaming to cassandra - 
docker exec -it cassandra cqlsh -u cassandra -p cassandra localhost 9042
```sql
USE my_keyspace;
select * from iss_data;
select count(*) from iss_data;


# cleaning data - 
select min(timestamp) from iss_data;
SELECT * FROM iss_data WHERE timestamp = '2024-03-28 07:46:03.000000+0000' ALLOW FILTERING;

DELETE FROM iss_data WHERE id = 86167844-3b9a-4a0a-b00a-1803fa6849a4;

```





# docker compose -f "Airflow/1.postgres_sql.yml" up -d
# note the name of the container
# chmod +x 5.Airflow_containers/script/entrypoint.sh
# both of following is going to take time to run because requrment.txt file is going to install each packages 
# docker compose -f "Airflow/2.airflow_webserver.yml" up -d
# docker compose -f "Airflow//3.airflow_scheduler.yml" up -d    