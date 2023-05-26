from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os

from dotenv import load_dotenv
from notion.find_relation import find_operator
from functions.console import log
from notion.check_notion_db_record_exists import check_notion_db_record_exists
from notion_client import Client

# Load environment variable
NOTION_DB_TRAVEL = os.getenv("NOTION_DB_TRAVEL")

load_dotenv()


def create_notion_db_record(notion: Client, page: dict) -> None:
    """
    Create a new Notion database record.

    Args:
    notion: Notion client instance.
    page: Page data to be added to the Notion database.

    Returns:
    None
    """
    # check if page already exists in Notion
    if check_notion_db_record_exists(notion, page):
        log("duplicate, skipping...", "warning")
        return

    try:
        log(f"Sending page to Notion...", "success")
        notion.pages.create(
            parent={"database_id": NOTION_DB_TRAVEL}, properties=page)
    except Exception as e:
        log(f"Failed to create record: {e}", "danger")


executor = ThreadPoolExecutor(max_workers=1)


def create_notion_db_record_background(notion: Client, page: dict):
    """
    Submit the function to be executed asynchronously in the background.

    Args:
    notion: Notion client instance.
    page: Page data to be added to the Notion database.

    Returns:
    concurrent.futures.Future: Future object that represents a computation 
    that hasn't necessarily completed yet.
    """
    future = executor.submit(create_notion_db_record, notion, page)
    return future
