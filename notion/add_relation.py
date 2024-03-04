from typing import Any, Dict
from notion_client import Client
from notion.find_relation import find_operator
from functions.console import log


def add_relation(notion: Client, record: Dict[str, Any], property: str, relation: str) -> Dict[str, Any]:
    """
    Adds a relation (another record) on the record's property.

    Args:
    notion: notion_client.Client instance.
    record: Dictionary representing the record to be updated.
    property: The property on the record to which the relation is to be added.
    relation: The relation to be added.

    Returns:
    record: Updated record with the new relation added.
    """
    operator = find_operator(notion, relation)
    if operator:
        record[property] = {"relation": [{"id": operator[0]}]}
    else:
        # Consider logging or raising an exception here.
        log(f"Warning: Unable to find relation '{relation}'.", "warning")

    return record
