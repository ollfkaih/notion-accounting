import datetime
import imaplib
import os
from email.header import decode_header
import email
import re
import quopri
from dateutil.parser import parse
from functions.console import log
from functions.get_html import get_data_from_html
from functions.mail_parsers.non_specific_dates import non_specific_dates
from functions.mail_parsers.specific_dates import specific_dates
from contextlib import closing

from functions.parse_date import parse_date
from typing import TypedDict, Optional


class RequiredTransactionDetails(TypedDict):
    name: str
    date_time: str
    cardholder_name: str
    bank_name: str
    card_number: str
    location: str
    foreign: bool


# Define another TypedDict for optional transaction details
class OptionalTransactionDetails(TypedDict, total=False):
    amount_nok: Optional[float]
    amount_try: Optional[float]
    amount_eur: Optional[float]
    amount_usd: Optional[float]
    amount_gbp: Optional[float]
    transaction_description: Optional[str]


# Combine the two using multiple inheritance
class TransactionDetails(RequiredTransactionDetails, OptionalTransactionDetails):
    pass


TEXT_PLAIN = "text/plain"
SUBJECT_FILTER = "Curve Receipt"


def get_details(text: str) -> TransactionDetails:
    # Define patterns for extracting information
    patterns = {
        "name": r"Hello\s+(\w+),",
        "location": r"at:\s*\n\s*(.+)\n",
        "amount_nok": r"(\d+\.\d+)\s+NOK",
        "amount_try": r"(\d+\.\d+)\s+TRY",
        "amount_eur": r"€(\d+\.\d+)\s",
        "amount_usd": r"\$(\d+\.\d+)\s",
        "amount_gbp": r"£(\d+\.\d+)\s",
        "date_time": r"(\d{2} \w+ \d{4} \d{2}:\d{2}:\d{2})",
        "cardholder_name": r"On this card:\s*\n\s*(.+)\n",
        "bank_name": r"\n\s*(\w+ Bank)\n",
        "card_number": r"XXXX-(\d+)",
        "transaction_description": r"appear on your bank statement as:\s*\n\s*(.+)\n",
    }

    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            extracted_data[key] = match.group(1).strip()

    if "card_number" in extracted_data:
        extracted_data["card_number"] = int(extracted_data["card_number"])
    if "amount_nok" in extracted_data:
        extracted_data["amount_nok"] = float(extracted_data["amount_nok"])
    if "amount_try" in extracted_data:
        extracted_data["amount_try"] = float(extracted_data["amount_try"])
    if "amount_eur" in extracted_data:
        extracted_data["amount_eur"] = float(extracted_data["amount_eur"])
    if "amount_usd" in extracted_data:
        extracted_data["amount_usd"] = float(extracted_data["amount_usd"])
    if "amount_gbp" in extracted_data:
        extracted_data["amount_gbp"] = float(extracted_data["amount_gbp"])
    extracted_data["foreign"] = (
        "amount_try" in extracted_data
        or "amount_eur" in extracted_data
        or "amount_usd" in extracted_data
        or "amount_gbp" in extracted_data
    )

    return extracted_data


# Example usage:
# Replace 'your_email_receipt_text_here' with your actual email receipt text.
# data = "your_email_receipt_text_here"
# extracted_vars = extract_data(data


def get_mails(number: int) -> list[TransactionDetails]:
    """
    This function connects to an email server, retrieves the last three emails, and parses their content.

    Args:
    number: int, the number of emails to fetch.

    Returns:
    parsed_data: list, contains parsed email data from the last three emails.
    """
    try:
        with closing(imaplib.IMAP4_SSL(os.getenv("EMAIL_IMAP"))) as mail:
            rv, data = mail.login(
                os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD")
            )
            if rv != "OK":
                log("Unable to log in to email server", "danger")
                return None

            mail.select("INBOX")

            # Get the list of email IDs
            result, data = mail.uid("search", None, "ALL")
            email_ids = data[0].split()

            # Get the latest three email IDs
            latest_email_ids = email_ids[-number:]

            # Parse the emails
            parsed_data = []
            email_uids = []
            for email_id in reversed(latest_email_ids):
                result, email_data = mail.uid("fetch", email_id, "(BODY[TEXT])")
                raw_email = email_data[0][1].decode("utf-8")

                if SUBJECT_FILTER not in raw_email:
                    mark_as_unread(email_id.decode("utf-8"))
                    continue

                # Parse the raw email
                email_message = email.message_from_string(raw_email)

                subject = None
                # Get the email part and decode it
                for part in email_message.walk():
                    if part.get_content_type() == TEXT_PLAIN:  # ignore attachments/html
                        byte_code = part.get_payload(decode=True)
                        if byte_code:
                            decoded_bytes = quopri.decodestring(byte_code)
                            email_text_content = decoded_bytes.decode("utf-8")
                            transaction_details = get_details(email_text_content)
                            transaction_details["uid"] = email_id.decode("utf-8")
                            parsed_data.append(transaction_details)
            return parsed_data

    except imaplib.IMAP4.error as e:
        log(f"An error occurred: {e}", "danger")
        return None


def archive_email(uid: str) -> None:
    """
    This function archives an email by moving it to the 'Archived' folder.

    Args:
    uid: str, the unique identifier of the email to be archived.

    Returns:
    None
    """
    try:
        with closing(imaplib.IMAP4_SSL(os.getenv("EMAIL_IMAP"))) as mail:
            rv, data = mail.login(
                os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD")
            )
            if rv != "OK":
                log("Unable to log in to email server", "danger")
                return None

            mail.select("INBOX")

            # Get the list of email IDs
            result = mail.uid("search", None, f"UID {uid}")

            # Copy the email to the 'Archived' folder
            result, _ = mail.uid("COPY", uid, "Archive")

            # If the copy was successful, delete the original email
            if result == "OK":
                mail.uid("store", uid, "+FLAGS", "\\Deleted")
                mail.expunge()
    except imaplib.IMAP4.error as e:
        log(f"An error occurred: {e}", "danger")
        return None


def mark_as_unread(uid: str) -> None:
    """
    This function marks an email as unread.

    Args:
    uid: str, the unique identifier of the email to be marked as unread.

    Returns:
    None
    """
    try:
        with closing(imaplib.IMAP4_SSL(os.getenv("EMAIL_IMAP"))) as mail:
            rv, data = mail.login(
                os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD")
            )
            if rv != "OK":
                log("Unable to log in to email server", "danger")
                return None

            mail.select("INBOX")

            # Get the list of email IDs
            result, data = mail.uid("search", None, f"UID {uid}")
            email_ids = data[0].split()

            # Mark the email as unread
            mail.uid("store", uid, "-FLAGS", "\\Seen")
    except imaplib.IMAP4.error as e:
        log(f"An error occurred: {e}", "danger")
        return None
