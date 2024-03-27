import logging
from cassandra.cluster import Cluster

def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS test_keyspace
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    print("Keyspace 'test_keyspace' created successfully!")

def create_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS test_keyspace.test_table (
        id UUID PRIMARY KEY,
        first_name TEXT,
        last_name TEXT
    );
    """)

    print("Table 'test_table' created successfully!")

def insert_data(session):
    try:
        session.execute("""
            INSERT INTO test_keyspace.test_table(id, first_name, last_name)
            VALUES (uuid(), 'John', 'Doe');
        """)
        logging.info("Data inserted successfully!")

    except Exception as e:
        logging.error(f'Could not insert data due to {e}')

def create_cassandra_connection():
    try:
        cluster = Cluster(['cassandra'])
        cas_session = cluster.connect('test_keyspace')
        return cas_session

    except Exception as e:
        logging.error(f"Could not create Cassandra connection due to {e}")
        return None

if __name__ == "__main__":
    session = create_cassandra_connection()

    if session is not None:
        create_keyspace(session)
        create_table(session)
        insert_data(session)

        session.shutdown()
