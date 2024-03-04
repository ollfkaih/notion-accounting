from datetime import datetime
from typing import Optional

from notion_client import Client
from functions.get_mails import TransactionDetails
from notion.find_relation import find_operator
from datetime import datetime, timezone, timedelta


def create_notion_page(notion, data: TransactionDetails) -> dict:
    merchant_id = [
        {"id": mid} for mid in find_operator(notion, data.get("location")) or []
    ]
    new_page = {
        "Beskrivelse": {
            "title": [{"text": {"content": data.get("location")}}],
        },
        "Dato": {
            "date": {
                "start": datetime.strptime(data.get("date_time"), "%d %B %Y %H:%M:%S")
                .replace(tzinfo=timezone(timedelta(hours=1)))
                .isoformat()  # time zone is GMT+1
            },
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
