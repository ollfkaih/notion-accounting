import os
from functions.console import log

from notion.cache import destroy_cache, get_database_data
import time


def find_operator(notion, text) -> list:
    print("Finding operator")
    operators = get_database_data(notion, os.getenv("NOTION_DB_MERCHANTS")).get(
        "results"
    )

    print("Operators", operators)

    matching_operator_ids = []

    for operator in operators:
        if len(operator["properties"]["Aliaser"]["rich_text"]) > 0:
            operator_name = operator["properties"]["Aliaser"]["rich_text"][0]["text"][
                "content"
            ]
            if operator_name.lower() in text.lower():
                matching_operator_ids.append(operator["id"])

    if len(matching_operator_ids) == 0:
        # create new operator
        new_page = notion.pages.create(
            parent={"database_id": os.getenv("NOTION_DB_MERCHANTS")},
            properties={
                "Navn": {"title": [{"text": {"content": text}}]},
                "Aliaser": {"rich_text": [{"text": {"content": text}}]},
            },
        )

        log("Created new operator", "success")
        destroy_cache(os.getenv("NOTION_DB_MERCHANTS"))
        return [new_page.get("id")]

    return matching_operator_ids
