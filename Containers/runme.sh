docker network create --driver bridge ISS_proj


docker compose -f "Kafka/docker-compose.yml" up -d

# go to http://192.168.1.111:9021/

# going to take time
docker compose -f "Airflow/docker-compose.yml" up -d
# go to http://192.168.1.111:8536/


docker compose -f "Spark/docker-compose.yml" up -d
# go to http://192.168.1.111:9537/

# --- testing -- 
docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/scripts/spark_test.py

docker exec -it spark-spark-master-1 bash -c 'cp /opt/bitnami/spark/scripts/data.csv /opt/bitnami/spark/data/data.csv'

docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/scripts/spark_test_csv.py


# kafka data to spark 
docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /opt/bitnami/spark/scripts/kafka_spark_stream.py



# Cassandra
docker compose -f "Cassandra/docker-compose.yml" up -d

# testing -- 


# Cassandra and spark conneciton test
# install dirvers 
docker exec -it spark-spark-master-1 bash
pip install cassandra-driver

sudo -H pip install cassandra-driver


docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/scripts/cassandra_conneciton_test.py

docker exec -it spark-spark-master-1 spark-submit --master spark://spark-master:7077 --packages com.datastax.spark:spark-cassandra-connector_2.12:3.4.0 /opt/bitnami/spark/scripts/cassandra_conneciton_test.py






# docker compose -f "Airflow/1.postgres_sql.yml" up -d
# note the name of the container
# chmod +x 5.Airflow_containers/script/entrypoint.sh
# both of following is going to take time to run because requrment.txt file is going to install each packages 
# docker compose -f "Airflow/2.airflow_webserver.yml" up -d
# docker compose -f "Airflow//3.airflow_scheduler.yml" up -d    