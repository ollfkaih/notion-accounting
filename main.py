import os

from dotenv import load_dotenv
from notion_client import Client
from functions.console import log

from functions.get_mails import archive_email, get_mails
from notion.create_notion_db_record import create_notion_db_record
from notion.create_notion_page import create_notion_page
from notion.find_relation import find_operator

MAX_EMAILS = 150

load_dotenv()  # Use context manager
notion = Client(auth=os.getenv("NOTION_KEY"))
transaction_data = get_mails(MAX_EMAILS)

if not transaction_data:
    log("No emails found", "danger")

for transaction in transaction_data:

    if not transaction:
        log("No emails found", "danger")
        continue

    log(
        f"Processing transaction: {transaction.get('location')} - {transaction.get('amount_nok')}NOK",
        "info",
    )

    page = create_notion_page(notion, transaction)

    if create_notion_db_record(notion, page):
        archive_email(transaction.get("uid"))
    else:
        mark_as_unread(transaction.get("uid"))
