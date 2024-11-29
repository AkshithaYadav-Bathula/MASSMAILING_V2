import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import base64

# SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@gmail.com'  # Your email address
SMTP_PASSWORD = 'your_email_password'  # Your email password or app-specific password

# Google API Configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'credentials.json'  # Google OAuth2 credentials file


def send_email_smtp(to, cc, bcc, subject, body):
    """
    Sends an email via SMTP using Gmail.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to
        msg['CC'] = cc
        msg['BCC'] = bcc
        msg['Subject'] = subject

        # Add the email body to the message
        msg.attach(MIMEText(body, 'plain'))

        # Create the SMTP server connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USER, SMTP_PASSWORD)

        # Send the email
        to_list = [to] + cc.split(',') + bcc.split(',')
        server.sendmail(SMTP_USER, to_list, msg.as_string())
        server.quit()

        return "Email sent successfully via SMTP!"

    except Exception as e:
        return f"An error occurred while sending email via SMTP: {str(e)}"


def send_email_gmail_api(to, cc, bcc, subject, body):
    """
    Sends an email using the Gmail API.
    """
    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is created automatically when the
        # authorization flow completes for the first time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart()
        message['to'] = to
        message['cc'] = cc
        message['bcc'] = bcc
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        # Send the email via Gmail API
        message = service.users().messages().send(userId='me', body=raw_message).execute()

        return "Email sent successfully via Gmail API!"

    except HttpError as error:
        return f"An error occurred while sending email via Gmail API: {str(error)}"


def send_email(to, cc, bcc, subject, body):
    """
    Chooses whether to use SMTP or Gmail API for sending an email.
    """
    # Attempt to send via SMTP first
    smtp_result = send_email_smtp(to, cc, bcc, subject, body)
    if "success" in smtp_result.lower():
        return smtp_result  # If SMTP is successful, return the result.

    # If SMTP fails, attempt to send via Gmail API
    gmail_result = send_email_gmail_api(to, cc, bcc, subject, body)
    return gmail_result


# Test sending an email
to = "recipient@example.com"
cc = "cc@example.com"
bcc = "bcc@example.com"
subject = "Test Subject"
body = "This is a test email body."

print(send_email(to, cc, bcc, subject, body))
