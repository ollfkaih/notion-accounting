from datetime import datetime
from typing import Optional

from notion_client import Client
from functions.get_mails import TransactionDetails
from notion.find_relation import find_operator
from datetime import datetime, timezone, timedelta
import pytz


def create_notion_page(notion, data: TransactionDetails) -> dict:
    merchant_id = [
        {"id": mid} for mid in find_operator(notion, data.get("location")) or []
    ]

    original_time = datetime.strptime(data.get("date_time"), "%d %B %Y %H:%M:%S")

    country = "Europe/Oslo"
    if data.get("foreign"):
        if "amount_eur" in data:
            country = "Europe/Berlin"
        if "amount_try" in data:
            country = "Europe/Istanbul"

    timezone = pytz.timezone(country)

    # Use localize method instead of replace
    localized_time = timezone.localize(original_time)

    # Convert to UTC
    utc_time = localized_time.astimezone(pytz.utc).isoformat()

    time = utc_time

    new_page = {
        "Beskrivelse": {
            "title": [{"text": {"content": data.get("location")}}],
        },
        "Dato": {
            "date": {"start": time},
        },
        "Beløp": {
            "number": data.get("amount_nok"),
        },
        "Opprinnelig beløp": {
            "number": data.get("amount_try"),
        },
        "Kort": {"select": {"name": str(data.get("card_number"))}},
        "Merchant": {
            "relation": merchant_id,
        },
    }

    return new_page
