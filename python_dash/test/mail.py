import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


# Email configuration

outlook_email = os.getenv('GMAIL_EMAIL')
outlook_password = os.getenv('GMAIL_PASSWORD')

gmail_email = os.getenv('GMAIL_EMAIL')

# Create a message
message = MIMEMultipart()
message["From"] = outlook_email
message["To"] = gmail_email
message["Subject"] = "Subject of the Email"
body = "Body of the email."
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
