import uuid
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from ISS_stream_data.request_data import RequestData
from ISS_stream_data.stream_data import ProduceData    #when want to import self made package then use the foldername.filename
import time


Reqdata = RequestData()
stream = ProduceData()

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 3, 16, 5, 7)
}

def stream_data():
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        data = Reqdata.get_data()
        stream.produce_data(data)
        time.sleep(10)


with DAG('ISS_automation',
        default_args=default_args,
        # schedule_interval='@daily',
        schedule_interval='*/4 * * * *',  # Run every 4 minutes
        catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
