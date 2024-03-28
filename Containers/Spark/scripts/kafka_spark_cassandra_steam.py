from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

import uuid
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark = SparkSession.builder \
    .appName("KafkaToCassandra") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .getOrCreate()


schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("longitude", StringType(), True),
    StructField("latitude", StringType(), True)
])


kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "ISS_API_DATA") \
    .load()


parsed_df = kafka_df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

generate_uuid = udf(lambda: str(uuid.uuid4()), StringType())

parsed_df_with_id = parsed_df.withColumn("id", generate_uuid())

query = parsed_df_with_id \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(lambda batch_df, batch_id: batch_df.write.format("org.apache.spark.sql.cassandra")
                   .options(table="iss_data", keyspace="my_keyspace").mode("append").save()) \
    .start()


query.awaitTermination()