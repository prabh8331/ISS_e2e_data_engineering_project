from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from python_mail.is_iss_overhead import ISSoverhead
from python_mail.is_night import IsNight    #when want to import self made package then use the foldername.filename
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

iss_overhead = ISSoverhead()
night = IsNight()

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 3, 16, 5, 7)
}

def send_mail():
    if iss_overhead.get_data() and night.get_data():
        # Email configuration 
        outlook_email = os.getenv('GMAIL_EMAIL')
        outlook_password = os.getenv('GMAIL_PASSWORD')
        gmail_email = os.getenv('GMAIL_EMAIL')
        
        # Create a message
        message = MIMEMultipart()
        message["From"] = outlook_email
        message["To"] = gmail_email
        message["Subject"] = "International Space Station"
        body = "Hello Prabh, Look up in the sky ISS is passing through. Enjoy this Space event."
        message.attach(MIMEText(body, "plain"))
        
        # Connect to the outlook Mail SMTP server
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Login to the outlook Mail SMTP server
        server.login(outlook_email, outlook_password)
        
        # Send the email
        server.sendmail(outlook_email, gmail_email, message.as_string())
        
        # Disconnect from the server
        server.quit()


with DAG('ISS_automation',
        default_args=default_args,
        # schedule_interval='@daily',
        schedule_interval='*/1 * * * *',  # Run every 4 minutes
        catchup=False) as dag:

    send_iss_mail = PythonOperator(
        task_id='send_iss_mail',
        python_callable=send_mail
    )
