import quopri
import re
from functions.create_flight_dict import create_flight_dict
from functions.console import log

from functions.parse_date import parse_date


def non_specific_dates(text):

    text = text.split("<html", 1)[0]  # Remove HTML
    text = text.split("Se flere flyreiser", 1)[0]  # Remove footer

    # Remove header
    text = text.split("Hei!", 1)[1]

    text = text.split(">")
    text = [s.replace('\r', '') for s in text]
    text = [s.replace('\n', '') for s in text]

    text = [element for element in text if element.strip()
            != "Direkte"]

    text = [element for element in text if element.strip()
            != "Billigst"]

    info = text[1:4]
    trips = text[4:]
    prices = []

    new_trips = []

    # Step by 5 because there are 4 elements and an empty string after every group
    for i in range(0, len(trips), 5):
        if "Akkurat nå er prisene" in trips[i] or "er en" in trips[i+1]:
            break
        group = trips[i:i+4]  # Get the next four elements
        new_trips.append(group)

    new_trips = [[s.replace('\xa0', ' ') for s in sublist]
                 for sublist in new_trips]

    for e in new_trips:
        e[0] = parse_date(e[0][1:])
        e[1] = e[1].split("Fra ")[1]
        e[1] = ''.join(char for char in e[1] if char.isdigit())
        e[1] = int(e[1])
        e[3] = e[3].split(" · ")
        e[3][0] = e[3][0].split(", ")
        del e[2]

    flag = False
    for element in trips:
        if "Akkurat nå er prisene" in element:
            flag = True

        if flag:
            prices.append(element)

    prices = [value for value in prices if value != '']
    prices = [s.replace('\xa0', ' ') for s in prices]
    prices = prices[2:4]
    prices = [re.findall(r'\d+', s.replace(' ', ''))
              for s in prices]
    prices = [item for sublist in prices for item in sublist]
    prices = [int(num) for num in prices]

    dict_list = []
    for flight in new_trips:
        new_dict_entry = create_flight_dict(
            journey=info[0].split("fra ")[1] + info[1],
            start=flight[0][0],
            end=flight[0][1],
            cabin=info[2].split(" · ")[3],
            new_price=flight[1],
            old_price=flight[1],
            duration=flight[2][3],
            airlines=flight[2][0],
            stops=flight[2][1],
            route=flight[2][2],
            type="Non specific",
            value=value(flight[1], prices)
        )
        dict_list.append(new_dict_entry)

    return dict_list


def value(price: int, priceStats: list[int]):
    if price < priceStats[0]:
        return "Cheap"
    elif price < priceStats[1]:
        return "Average"
    else:
        return "Expensive"
