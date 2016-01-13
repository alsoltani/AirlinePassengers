import os
import pandas as pd
import numpy as np

from datetime import timedelta

path = os.getcwd()

# Oil data.

baril_price = pd.read_csv(path + "/data/external/DCOILWTICO.csv").\
    replace(".", np.nan).convert_objects(convert_numeric=True)

baril_price["DATE"] = pd.to_datetime(baril_price["DATE"])
baril_price["VALUE"] = baril_price["VALUE"].interpolate()

baril_price = baril_price.rename(columns={"DATE": "DateOfDeparture", "VALUE": "BarilPrice"}).\
    set_index("DateOfDeparture")

# Public data.

public = pd.read_csv(path + "/data/public/public_train.csv")
public['DateOfDeparture'] = pd.to_datetime(public['DateOfDeparture'])


# Create date of booking.

def date_of_booking(datetime_of_departure, weeks_to_departure):
        return datetime_of_departure - timedelta(weeks=weeks_to_departure)

public['DateOfBooking'] = public.apply(lambda r:
        date_of_booking(r['DateOfDeparture'], r["WeeksToDeparture"]), axis=1)
public['DateOfBooking'] = public['DateOfBooking'].apply(lambda x: x.strftime("%Y-%m-%d"))
public['DateOfBooking'] = pd.to_datetime(public['DateOfBooking'])

# Merge data. Sort, interpolate for missing values, and reindex.

merged = public.join(baril_price, on="DateOfBooking").sort("DateOfBooking")
merged["BarilPrice"] = merged["BarilPrice"].interpolate()

merged = merged.reindex(xrange(len(merged)))

merged[["DateOfDeparture", "BarilPrice"]].\
    to_csv(path + "/Submission/baril_booking.csv", index=False)
