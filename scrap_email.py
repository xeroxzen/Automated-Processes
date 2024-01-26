import imaplib
import email
from email.header import decode_header

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL('your_email_server.com')
mail.login('your_email@example.com', 'your_password')

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
