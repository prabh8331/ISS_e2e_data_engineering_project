from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkTest") \
    .getOrCreate()

# Define the schema for the Kafka messages
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("longitude", StringType(), True),
    StructField("latitude", StringType(), True)
])

# Read messages from the Kafka topic
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "ISS_API_DATA") \
    .load()

# Parse the value column as JSON and select the required fields
parsed_df = kafka_df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Print the parsed data
query = parsed_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
