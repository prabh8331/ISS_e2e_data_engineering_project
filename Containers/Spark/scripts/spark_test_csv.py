from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, when

# Create a Spark session
spark = SparkSession.builder \
    .appName("SparkTest") \
    .getOrCreate()

# Read data from CSV file
df = spark.read.csv("file:///opt/bitnami/spark/data/data.csv", header=True, inferSchema=True)

# Split the 'name' column into 'first_name' and 'last_name'
df = df.withColumn("first_name", split(col("name"), " ")[0])
df = df.withColumn("last_name", split(col("name"), " ")[1])
df = df.drop("name")


# Show the processed data
df.show()

# Stop the Spark session
spark.stop()
