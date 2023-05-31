import os
from functions.console import log

from notion.cache import destroy_cache, get_database_data


def find_operator(notion, text):
    operators = get_database_data(notion, os.getenv(
        'NOTION_DB_OPERATOR')).get("results")
    matching_operator_ids = []

    for operator in operators:
        if len(operator["properties"]["alias"]["rich_text"]) > 0:
            operator_name = operator["properties"]["alias"]["rich_text"][0]["text"]["content"]
            if operator_name.lower() in text.lower():
                matching_operator_ids.append(operator["id"])

    if len(matching_operator_ids) == 0:
        # create new operator
        new_page = notion.pages.create(
            parent={"database_id": os.getenv("NOTION_DB_OPERATOR")},
            properties={
                "Navn": {"title": [{"text": {"content": text}}]},
                "alias": {"rich_text": [{"text": {"content": text}}]}
            }
        )

        log("Created new operator", "success")
        destroy_cache(os.getenv("NOTION_DB_OPERATOR"))
        print(new_page.get("id"))
        return [new_page.get("id")]

    return matching_operator_ids


def find_destination(notion, text):
    destinations = get_database_data(
        notion, os.getenv("NOTION_DB_DESTINATION")).get("results")

    matching_destination_ids = []

    for destination in destinations:
        destination_name = destination["properties"]["Name"]["title"][0]["text"]["content"]
        if destination_name.lower() in text.lower():
            matching_destination_ids.append(destination["id"])

    return matching_destination_ids
