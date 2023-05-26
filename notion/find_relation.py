import os

from notion.cache import get_database_data


def find_operator(notion, text):
    operators = get_database_data(notion, os.getenv(
        'NOTION_DB_OPERATOR')).get("results")
    matching_operator_ids = []

    for operator in operators:
        if len(operator["properties"]["alias"]["rich_text"]) > 0:
            operator_name = operator["properties"]["alias"]["rich_text"][0]["text"]["content"]
            if operator_name.lower() in text.lower():
                matching_operator_ids.append(operator["id"])

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
