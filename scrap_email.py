import imaplib
import email
from email.header import decode_header
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail credentials
email_address = 'andilembele020@gmail.com'
credentials_file = './client_secret_643679285698-rug9n33k7ht3d6j55nkbdbplivcf09q8.apps.googleusercontent.com.json'

# Set up the Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Authenticate using OAuth
flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
credentials = flow.run_local_server(port=0)

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_address, credentials.token)

mail.select('inbox')

status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()

# Fetch and parse emails
for email_id in email_ids:
    _, msg_data = mail.fetch(email_id, '(RFC822)')
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Relevant information (e.g., subject, sender, body)
    subject, encoding = decode_header(msg["Subject"])[0]
    subject = subject.decode(encoding) if encoding else subject

    sender = msg.get("From")
    print("Subject:", subject)
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    # Save the attachment in the current directory
                    with open(filename, "wb") as f:
                        f.write(part.get_payload(decode=True))
            else:
                # Email body
                body = part.get_payload(decode=True).decode()
    else:
        # Extract the email body
        body = msg.get_payload(decode=True).decode()

mail.logout()
