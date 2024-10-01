import os
from notion.cache import get_database_data

from functions.console import log
from datetime import datetime, timedelta


def check_notion_db_record_exists(notion, page) -> bool:

    existing_record = False
    sixty_days_ago = datetime.now() - timedelta(days=60)

    sixty_days_ago_str = sixty_days_ago.strftime("%Y-%m-%d")

    filter_params = {"property": "Dato", "date": {"after": sixty_days_ago_str}}

    data = get_database_data(
        notion, os.getenv("NOTION_DB_TRANSACTIONS"), filter_params=filter_params
    )

    for page_record in data["results"]:

        page_record_date = page_record["properties"]["Dato"]["date"]["start"]

        try:
            page_record_time = page_record_date.split("T")[1]
            page_record_date = page_record_date.split("T")[0]
            page_record_hours_minutes = page_record_time.split(":")[0:2]

            page_record_price = page_record["properties"]["Beløp"]["number"]
            page_record_merchant = page_record["properties"]["Beskrivelse"]["title"][0][
                "text"
            ]["content"]

            page_date = page["Dato"]["date"]["start"]
            page_time = page_date.split("T")[1]
            page_date = page_date.split("T")[0]
            page_hours_minutes = page_time.split(":")[0:2]

            page_price = page["Beløp"]["number"]
            page_merchant = page["Beskrivelse"]["title"][0]["text"]["content"]

            identical_date = page_date == page_record_date
            identical_time = page_hours_minutes == page_record_hours_minutes
            identical_price = page_price == page_record_price
            identical_merchant = page_merchant == page_record_merchant

            if identical_date and identical_time and identical_price and identical_merchant:
                existing_record = True
                break
        except:
            # there was an entry without proper date, so we ignore it
            log(page_record["properties"]["Beskrivelse"][title][0]["text"]["content"] + " is missing date")
            pass



    return existing_record
