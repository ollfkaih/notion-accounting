import datetime
import imaplib
import os
from email.header import decode_header
import email
import quopri
from dateutil.parser import parse
from functions.mail_parsers.non_specific_dates import non_specific_dates
from functions.mail_parsers.specific_dates import specific_dates
from contextlib import closing

from functions.parse_date import parse_date

TEXT_PLAIN = "text/plain"
SUBJECT_LINE = "Subject"
SPECIFIC_ROUTE = "Ruten du sporer"


def get_mails(number: int):
    """
    This function connects to an email server, retrieves the last three emails, and parses their content.

    Args:
    number: int, the number of emails to fetch.

    Returns:
    parsed_data: list, contains parsed email data from the last three emails.
    """
    with closing(imaplib.IMAP4_SSL(os.getenv("EMAIL_IMAP"))) as mail:
        mail.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
        mail.select("INBOX")

        # Get the list of email IDs
        result, data = mail.uid('search', None, "ALL")
        email_ids = data[0].split()

        # Get the latest three email IDs
        latest_email_ids = email_ids[-number:]

        # Parse the emails
        parsed_data = []
        for email_id in reversed(latest_email_ids):
            result, email_data = mail.uid('fetch', email_id, '(BODY[TEXT])')
            raw_email = email_data[0][1].decode("utf-8")

            # Parse the raw email
            email_message = email.message_from_string(raw_email)

            # Get the email part and decode it
            subject = ""
            for part in email_message.walk():
                if part.get_content_type() == TEXT_PLAIN:  # ignore attachments/html
                    byte_code = part.get_payload(decode=True)
                    if byte_code:
                        decoded_bytes = quopri.decodestring(byte_code)
                        email_text_content = decoded_bytes.decode("utf-8")
                        for line in email_text_content.split("\n"):
                            if SUBJECT_LINE in line:
                                subject = line.split(f"{SUBJECT_LINE}: ")
                                if len(subject) > 1:
                                    subject = subject[1]
                                    if SPECIFIC_ROUTE in subject:
                                        parsed_data.append(
                                            non_specific_dates(email_text_content))
                                    else:
                                        parsed_data.append(
                                            specific_dates(email_text_content))

        return parsed_data
