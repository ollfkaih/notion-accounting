
from babel.dates import get_month_names
import datetime


from babel.dates import get_month_names
import datetime


from babel.dates import get_month_names
import datetime


from babel.dates import get_month_names
import datetime


def parse_date(date_string: str):

    # Get both full and abbreviated month names in Norwegian
    months_no_wide = get_month_names('wide', locale='no')
    months_no_abbr = get_month_names('abbreviated', locale='no')

    # Create a dictionary to map Norwegian month names to numbers
    month_to_num = {name.lower(): i for i,
                    name in months_no_wide.items() if name}
    month_to_num.update(
        {name.lower(): i for i, name in months_no_abbr.items() if name})

    # Split the string into start and end date strings
    start_date_string, end_date_string = date_string.split('–')

    # Extract the year
    current_year = datetime.datetime.now().year

    # Remove day-of-week and split by spaces to get day and month
    start_day_month = start_date_string.split('.', 1)[1].strip().split(' ')
    end_day_month = end_date_string.split('.', 1)[1].strip().split(' ')

    # Ensure there are two elements in the lists
    if len(start_day_month) != 2 or len(end_day_month) != 2:
        raise ValueError('Invalid date string format')

    start_day, start_month = start_day_month
    end_day, end_month = end_day_month

    # Convert day and month to date (assuming current year)
    start_date = datetime.date(
        current_year, month_to_num[start_month.lower()], int(start_day.replace(".", "")))
    end_date = datetime.date(
        current_year, month_to_num[end_month.lower()], int(end_day.replace(".", "")))

    # Convert to ISO 8601 format
    start_date_iso = start_date.isoformat()
    end_date_iso = end_date.isoformat()

    return [start_date_iso, end_date_iso]
