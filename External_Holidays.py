import os
import holidays as holi
import pandas as pd

path = os.getcwd()

states = {"DFW": "TX",
          "LAX": "CA",
          "ORD": "IL",
          "DEN": "CO",
          "MCO": "FL",
          "IAH": "TX",
          "MIA": "FL",
          "ATL": "GA",
          "LGA": "NY",
          "SEA": "WA",
          "PHX": "AZ",
          "CLT": "NC",
          "DTW": "MI",
          "LAS": "NV",
          "EWR": "NJ",
          "MSP": "MN",
          "BOS": "MA",
          "PHL": "PA",
          "SFO": "CA",
          "JFK": "NY"}


public = pd.read_csv(path + "/data/public/public_train.csv")
public['DateOfDeparture'] = pd.to_datetime(public['DateOfDeparture'])


def is_holidays(datetime_to_departure, airport_code):

    if datetime_to_departure in holi.US(state=states[airport_code],
                                        years=datetime_to_departure.year):
        return 1
    else:
        return 0

public["IsHoliday_Arrival"] = public.\
    apply(lambda r: is_holidays(r["DateOfDeparture"], r["Arrival"]), axis=1)

public["IsHoliday_Departure"] = public.\
    apply(lambda r: is_holidays(r["DateOfDeparture"], r["Departure"]), axis=1)

public[["IsHoliday_Arrival", "IsHoliday_Departure", "DateOfDeparture"]].\
    to_csv(path + "/Submission/holidays.csv", index=False)
