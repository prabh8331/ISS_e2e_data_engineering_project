from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect('my_keyspace')

# Create the iss_data table
session.execute("""
    CREATE TABLE IF NOT EXISTS iss_data (
        id UUID PRIMARY KEY,
        timestamp TIMESTAMP,
        longitude FLOAT,
        latitude FLOAT
    );
""")

# Insert the values
session.execute("""
    INSERT INTO iss_data (id, timestamp, longitude, latitude)
    VALUES (uuid(), '2024-03-28 07:46:03', 77.1159, 26.7929);
""")

session.shutdown()
