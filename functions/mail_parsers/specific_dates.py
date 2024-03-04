import quopri
import re
from functions.create_flight_dict import create_flight_dict

from functions.parse_date import parse_date


def specific_dates(text):

    for i in range(len(text)):
         print(i, text[i])

    flight_list_dict = []
    for i in range(0, len(text), 4):

        metadata = text[i].split(" ·")
        try:
            old_price = int(metadata[-1].split("kr")[-1])
        except:
            print("Not a valid old price, skipping")
            continue
        datearr = metadata[0].split(".")
        print(datearr)
        journey = datearr[0][0:-3]
        #date = datearr[0][-3:] + "." + datearr[1] + \
        #    "." + datearr[2] + "." + datearr[3] + "." + \
        #    datearr[4].replace("Tur/retur", "")

        #if len(date) < len("ons. 2. apr.-ons. 2. sep."):
        #    date = datearr[0][-3:] + "." + datearr[1] + \
        #        "." + datearr[2] + "." + datearr[3] + "." + \
        #        datearr[4] + "." + datearr[5] + "."

        # ons. 2. apr.-ons. 2. sep.
        #date = parse_date(date)

        # loop three times
        for j in range(3):
            flight = text[i+j+1]

            hours = None
            if flight[13:15] == "+1":
                hours = flight[0:15]
                flight = flight[15:]

            else:
                hours = flight[0:13]
                flight = flight[13:]

            flight = flight.split(" ·")

            print(flight)
            airlines = flight[0].split(", ")
            try:
                stops = flight[1]
            except:
                stops = "0 stopp"
            try:
                route, price = flight[2].split("kr")
            except:
                print("Not a valid route, skipping")
                continue

            flight_list_dict.append(create_flight_dict(
                journey=journey,
                start="2023-08-13",#date[0],
                end="2023-08-29",#date[1],
                cabin="Unknown",
                new_price=int(price),
                old_price=old_price,
                duration=hours,
                airlines=airlines,
                stops=stops,
                route=route,
                type="Specific",
                value="Unknown"
            ))

    return flight_list_dict
