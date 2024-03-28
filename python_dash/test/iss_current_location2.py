import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
from datetime import datetime, timedelta
import pytz

# Fetch current location of ISS
response = requests.get(url="http://api.open-notify.org/iss-now.json")
data = response.json()
iss_longitude = float(data["iss_position"]["longitude"])
iss_latitude = float(data["iss_position"]["latitude"])

# My currnet location 
my_latitude = 18.5894739
my_longitude = 74.0105505

#Check if ISS position is within +5 or -5 degrees of my position to verify if ISS is present to my visible sky
def is_iss_overhead():
    if (my_latitude-5 <= iss_latitude <= my_latitude+5) and ( my_longitude-5 <= iss_longitude <= my_longitude+5):
        return True
    else:
        return False


# check if night time in my location using sunrise-sunset API
parameters = {
    "lat" : my_latitude, 
    "lng" : my_longitude, 
    "formatted" : 0,
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)

data = response.json()

timezone_utc = pytz.timezone('UTC') 
timezone_ist = pytz.timezone('Asia/Kolkata')

sunset =  datetime.fromisoformat(data["results"]["sunset"]).replace(tzinfo=timezone_utc).astimezone(timezone_ist)
sunrise =  datetime.fromisoformat(data["results"]["sunrise"]).replace(tzinfo=timezone_utc).astimezone(timezone_ist) + timedelta(days=1)

time_now = datetime.now(timezone_ist)

def is_night():
    if time_now > sunset and time_now < sunrise:
        return True
    else:
        return False


if is_iss_overhead() and is_night():
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


