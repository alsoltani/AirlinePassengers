import os
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
from datetime import timedelta

path = os.getcwd()
airports = ['DFW', 'LAX', 'ORD', 'DEN', 'MCO', 'IAH', 'MIA', 'ATL', 'LGA',
            'SEA', 'PHX', 'CLT', 'DTW', 'LAS', 'EWR', 'MSP', 'BOS', 'PHL',
            'SFO', 'JFK']


def clean_data(data_path):

    # Find WBAN codes for airports.

    stations = pd.read_csv(data_path + "station.txt",
                           sep="|")[["WBAN", "CallSign"]]
    stations = stations[stations["CallSign"].isin(airports)]

    wban_list = stations["WBAN"].values.tolist()
    wban_dict = stations.set_index("WBAN").to_dict()["CallSign"]

    # Import external weather data.
    # Select only data from studied airports.

    weather = pd.read_csv(data_path + "daily.txt")\
        .replace("M", np.nan).replace("  T", 0.0)
    weather = weather[weather["WBAN"].isin(wban_list)].\
        convert_objects(convert_numeric=True).reset_index(drop=True)

    # Drop Depth, Water1 and SnowFall. They have almost no values :
    # weather["Depth"].unique() >> array([nan, '0'], dtype=object).

    weather = weather.drop(["Depth", "Water1", "SnowFall",
                            "DepthFlag", "Water1Flag", "SnowFallFlag"], axis=1)

    # Label encoding on categorical variables.

    le = LabelEncoder()
    categorical_variables = []

    for y in weather.columns:
        if weather[y].dtype != np.float64 and weather[y].dtype != np.int64:
            categorical_variables.append(y)
            weather[y] = le.fit_transform(weather[y])

    # Drop unsignificant colums.
    # weather = weather.drop([c for c in weather.columns if "Flag" in c], axis=1)

    for c in categorical_variables:
        if len(weather[c].unique()) < 5:
            weather = weather.drop([c], axis=1)

    # Fill missing values with median.
    # weather.isnull().sum()

    repl = weather.groupby("WBAN").transform('mean')
    weather.fillna(repl, inplace=True)

    # Map and rename columns.

    weather["WBAN"] = weather["WBAN"].map(wban_dict)
    weather["YearMonthDay"] = pd.to_datetime(weather["YearMonthDay"], format="%Y%m%d")
    weather = weather.rename(columns={'YearMonthDay': 'Date', 'WBAN': 'Airport'})

    return weather


def join_cleaned_data():

    # Concatenate cleaned data for various recordings.

    directories = [f for f in os.listdir(path + "/data/external")
               if "QCLCD" in f and ".zip" not in f]

    yearmonth_id = directories[0][5:]
    data_path = path + "/data/external/" + directories[0] + "/" + yearmonth_id
    full_weather_df = clean_data(data_path)

    for a in directories[1:]:

        yearmonth_id = a[5:]
        data_path = path + "/data/external/" + a + "/" + yearmonth_id
        full_weather_df = full_weather_df.append(clean_data(data_path))

    return full_weather_df


def group_data():

    # Merge on Departure.

    """data = pd.read_csv(path + "/data/public/public_train.csv")[["DateOfDeparture", "Departure"]]
    data['DateOfDeparture'] = pd.to_datetime(data['DateOfDeparture'])

    departure = join_cleaned_data().rename(columns={'Date': 'DateOfDeparture', 'Airport': 'Departure'})
    merged_dept = pd.merge(data, departure, on=["DateOfDeparture", "Departure"])
    merged_dept.columns = [c + "_Departure" if c not in ["DateOfDeparture", "Departure"] else c
                           for c in merged_dept.columns]
    merged_dept = merged_dept.drop(["DateOfDeparture", "Departure"], axis=1)"""

    # Merge on Arrival.

    data = pd.read_csv(path + "/data/public/public_train.csv")[["DateOfDeparture", "Arrival"]]
    data['DateOfDeparture'] = pd.to_datetime(data['DateOfDeparture'])

    arrival = join_cleaned_data().\
        rename(columns={'Date': 'DateOfDeparture', 'Airport': 'Arrival'}).\
        set_index("DateOfDeparture")

    merged_arrv = pd.merge(data, arrival, on=["DateOfDeparture", "Arrival"], how="left")

    # Rename and drop columns.

    merged_arrv.columns = [c + "_Arrival" if c not in ["DateOfDeparture",
                                                       "DateOfArrival",
                                                       "Arrival",
                                                       "WeeksToDeparture"]
                           else c
                           for c in merged_arrv.columns]
    print merged_arrv
    merged_arrv = merged_arrv.drop(["Arrival"], axis=1)

    # Concatenate the two fields.
    # merged_all = pd.concat([merged_arrv, merged_dept], axis=1)

    merged_all = merged_arrv.\
        convert_objects(convert_numeric=True)
    merged_all.to_csv(path + "/Submission/temperatures.csv")

group_data()
