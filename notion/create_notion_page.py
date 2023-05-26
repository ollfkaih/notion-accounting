from datetime import date
from typing import Optional


def create_notion_page(journey: str, route: str, old_price: int, new_price: int, operator, start_date, end_date, duration: str, stopp: str, destination, trend, value, cabin, type):

    new_page = {
        "Route": {"title": [{"text": {"content": journey}}]},
        "Price change": {"number": old_price - new_price},
        "New price": {"number": new_price},
        "Operator": {"relation": operator},
        "Date": {"date": {"start": start_date, "end": end_date}},
        "Duration": {"rich_text": [{"text": {"content": duration}}]},
        "Airports": {"rich_text": [{"text": {"content": route}}]},
        "Stopp": {"rich_text": [{"text": {"content": stopp}}]},
        "Old price": {"number": old_price},
        "Destination": {"relation": destination},
        "Trend": {"relation": trend},
        "Value": {"relation": value},
        "Cabin": {"select": {"name": cabin}},
        "Type": {"select": {"name": type}},
    }

    return new_page
