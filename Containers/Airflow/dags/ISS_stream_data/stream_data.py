import json
from kafka import KafkaProducer
import time
import logging

class ProduceData:
    def produce_data(self, data_input):
        producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)  # here this is going to run inside the docker container and inside the netowrk the port become 29092
        
        try: 
            producer.send('ISS_API_DATA', json.dumps(data_input).encode('utf-8'))
        except Exception as e:
            logging.error(f'An Error occured: {e}')

