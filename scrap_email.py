import imaplib
import email
from email.header import decode_header
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Set your Gmail credentials
email_address = 'andilembele020@gmail.com'
credentials_file = 'path/to/credentials.json'  # You need to create a credentials file using Google Cloud Console

# Set up the Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Authenticate using OAuth
flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
credentials = flow.run_local_server(port=0)

# Connect to the Gmail IMAP server
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_address, credentials.token)

# Select the mailbox you want to work with (e.g., 'inbox')
mail.select('inbox')

# Search for all emails
status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()

# Fetch the emails and parse them
for email_id in email_ids:
    _, msg_data = mail.fetch(email_id, '(RFC822)')
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Extract relevant information (e.g., subject, sender, body)
    subject, encoding = decode_header(msg["Subject"])[0]
    subject = subject.decode(encoding) if encoding else subject

    sender = msg.get("From")

    # Process the email content as needed
    # ...

# Logout and close the connection
mail.logout()
