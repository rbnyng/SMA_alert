import yfinance as yf
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Define a function to read the last state
def read_last_state(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    return None

# Define a function to write the current state
def write_current_state(file_path, state):
    with open(file_path, 'w') as file:
        file.write(state)

# Path to the state file
state_file_path = 'state.txt'

# Read the last state
last_state = read_last_state(state_file_path)

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

latest_data = data.tail(1)
sma_15 = latest_data['SMA_15'].item()
sma_190 = latest_data['SMA_190'].item()

crossed_above = sma_15 > sma_190
crossed_below = sma_15 < sma_190

current_state = 'above' if sma_15 > sma_190 else 'below'

if current_state != last_state:
    # Cross-over detected, send an email
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

    write_current_state(state_file_path, current_state)
