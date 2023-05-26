import quopri

from functions.parse_date import parse_date


def specific_dates(text):
    text = text.split("<html", 1)[0]
    text = text.split("Prisene ble oppdatert", 1)[0]
    text = text.split("destinasjoner og datoer:", 1)[1]
    text = text.split("Vis alle flyreisene")

    parsed_data = []
    for e in text:
        e = e.split("\n")

        e = [element.replace('> ', '').replace(
            '>', '') for element in e if element.replace('> ', '').replace('>', '')]

        e = [element.replace('\r\n', '').replace(
            '\xa0', '') for element in e]

        e = [item.strip() for item in e if item.strip()]

        if len(e) == 0:
            continue

        destination = e[0]
        dates = parse_date(e[1])
        oldPrice = int(e[4][2:].replace(">", ""))
        e = e[5:]

        # make every third element a new list
        e = [e[i:i + 3] for i in range(0, len(e), 3)]

        parsed_data.append([destination, dates, oldPrice, e])

    flights_dict = []
    for destination in parsed_data:

        destination_name = destination[0]
        dates = destination[1]
        oldPrice = destination[2]

        for flight in destination[3]:

            airline_info = flight[1].split(' · ')
            airlines = airline_info[0].split(", ")

            flight_dict = {
                "Journey": destination_name,
                "Start Date": dates[0],
                "End Date": dates[1],
                "Ticket Info": "unknown",
                "New Price": int(flight[2][2:].replace(">", "")),
                "Old Price": int(oldPrice),
                "Duration": "Unknown",
                "Airlines": airlines,
                "Stops": airline_info[1],
                "Route": airline_info[2],
                "Type": "Specific",
                "Value": "Unknown",
                "Cabin": "Unknown",
            }
            flights_dict.append(flight_dict)
    return flights_dict
