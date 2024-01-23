import yfinance as yf
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Check for test email environment variable
if os.environ.get('SEND_TEST_EMAIL') == 'true':
    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ['SENDER_EMAIL']
    sender_password = os.environ['SENDER_PASSWORD']
    receiver_email = os.environ['RECEIVER_EMAIL']

    # Create the email message
    message = MIMEMultipart()
    message['Subject'] = 'Test Email'
    message['From'] = sender_email
    message['To'] = receiver_email
    body = 'This is a test email from SMA Crossover Checker.'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

# Fetch historical data for VTI
data = yf.download('VTI', start='2000-01-01')

# Calculate 20-day and 200-day SMAs
data['SMA_15'] = data['Close'].rolling(window=15).mean()
data['SMA_190'] = data['Close'].rolling(window=190).mean()

# Check for crossover
latest_data = data.tail(1)
if latest_data['SMA_15'].item() > latest_data['SMA_190'].item():
    # Cross-over detected, send an email
    # Email setup here (will be detailed next)

    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    
    if not sender_email or not sender_password:
        raise ValueError("Email credentials are not set in environment variables.")
        
    # Create the email message
    message = MIMEMultipart()
    message['Subject'] = 'VTI 15-day SMA Crossed Over 190-day SMA'
    message['From'] = sender_email
    message['To'] = receiver_email
    body = 'The 15-day SMA of VTI has crossed over its 190-day SMA.'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
