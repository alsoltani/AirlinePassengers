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

# Merge data. Sort, interpolate for missing values, and reindex.

merged = public.join(baril_price, on="DateOfDeparture").sort("DateOfDeparture")
merged["BarilPrice"] = merged["BarilPrice"].interpolate()

merged = merged.reindex(xrange(len(merged)))

merged[["DateOfDeparture", "BarilPrice"]].\
    to_csv(path + "/Submission/baril_departure.csv", index=False)
