from is_iss_overhead import ISSoverhead
from is_night import IsNight
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

iss_overhead = True
night = True


if iss_overhead and night:
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