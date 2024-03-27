from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder \
    .appName("SparkTest") \
    .getOrCreate()


data = [("Alice", 30), ("Bob", 25), ("Catherine", 35)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Perform some processing
processed_df = df.withColumn("Category", when(col("Age") < 30, "Young").otherwise("Old"))

# Show the processed data
processed_df.show()

# Stop the Spark session
spark.stop()