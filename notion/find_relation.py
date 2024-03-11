import os
from functions.console import log

from notion.cache import destroy_cache, get_database_data
import json


def find_operator(notion, text) -> list:
    operators = get_database_data(notion, os.getenv("NOTION_DB_MERCHANTS")).get(
        "results"
    )
    # stringify as json

    matching_operator_ids = []

    for operator in operators:
        if len(operator["properties"]["Aliaser"]["rich_text"]) > 0:
            operator_name = operator["properties"]["Aliaser"]["rich_text"][0]["text"][
                "content"
            ]
            # look for partial match
            operator_parts = operator_name.lower().split(" ")
            match = 0
            for word in operator_parts:
                if len(word) >= 3 and word in text.lower():
                    match += 1
            if match >= 2:
                log(
                    f"Found operator: {operator['properties']['Navn']['title'][0]['plain_text']}",
                    "info",
                )
                matching_operator_ids.append(operator["id"])
                return matching_operator_ids

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
